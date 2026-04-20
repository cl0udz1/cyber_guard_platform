"""
Purpose:
    Account registration and login endpoints for user and organization access.
Inputs:
    Registration/login payloads and authenticated principal context.
Outputs:
    Tokens and current-user profile responses.
Dependencies:
    Route dependencies, security helpers, SQLAlchemy models, and auth schemas.
TODO Checklist:
    - [ ] Add invitation and password reset endpoints later.
    - [ ] Move token refresh and session revocation into a later auth phase.
"""

from datetime import datetime, timezone
from hashlib import sha256
from hmac import compare_digest

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_principal
from app.core.config import get_settings
from app.core.permissions import choose_higher_role
from app.core.security import create_access_token
from app.db.base import Base
from app.db.session import engine, get_db
from app.models import Membership, Organization, User, Workspace
from app.schemas.auth import CurrentPrincipal, LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import MembershipSummary, UserProfileResponse
from app.utils.constants import DEFAULT_ORGANIZATION_ID, DEFAULT_WORKSPACE_ID

router = APIRouter(prefix="/auth", tags=["auth"])

_tables_ready = False


def _ensure_auth_tables() -> None:
    """Create ORM tables on first use so the scaffold works without migrations."""
    global _tables_ready
    if _tables_ready:
        return
    Base.metadata.create_all(bind=engine)
    _tables_ready = True


def _build_display_name(email: str) -> str:
    """Create a readable name from the local part of an email address."""
    local_part = email.split("@", maxsplit=1)[0]
    return local_part.replace(".", " ").replace("_", " ").title()


def _membership_summary_from_model(membership: Membership) -> MembershipSummary:
    """Convert one membership row into the public response shape."""
    return MembershipSummary(
        organization_id=membership.organization_id,
        workspace_id=membership.workspace_id,
        role=membership.role,
    )


def _hash_password(password: str) -> str:
    """Create a deterministic local password digest for scaffold auth."""
    return sha256(password.encode("utf-8")).hexdigest()


def _verify_password(password: str, password_digest: str) -> bool:
    """Compare a submitted password with the stored scaffold digest."""
    return compare_digest(_hash_password(password), password_digest)


def _serialize_user_profile(user: User) -> UserProfileResponse:
    """Build the API profile response from a loaded user record."""
    memberships = sorted(
        (_membership_summary_from_model(membership) for membership in user.memberships),
        key=lambda membership: (
            membership.organization_id,
            membership.workspace_id or "",
            membership.role,
        ),
    )
    effective_role = choose_higher_role(user.platform_role, *(membership.role for membership in memberships))
    return UserProfileResponse(
        id=user.id,
        display_name=user.display_name,
        email=user.email,
        platform_role=effective_role,
        memberships=memberships,
        created_at=user.created_at,
    )


def _get_user_with_memberships(
    db: Session,
    *,
    user_id: str | None = None,
    email: str | None = None,
) -> User | None:
    """Load a user record and its memberships for profile and auth flows."""
    statement = select(User).options(selectinload(User.memberships))
    if user_id is not None:
        statement = statement.where(User.id == user_id)
    elif email is not None:
        statement = statement.where(User.email == email)
    else:
        raise ValueError("Either user_id or email is required.")
    return db.scalar(statement)


def _get_or_create_demo_org_and_workspace(db: Session) -> tuple[Organization, Workspace]:
    """Keep a deterministic demo org/workspace available for scaffold users."""
    organization = db.get(Organization, DEFAULT_ORGANIZATION_ID)
    if organization is None:
        organization = Organization(
            id=DEFAULT_ORGANIZATION_ID,
            name="Cyber Guard Demo Org",
            slug="cyber-guard-demo-org",
            sector="education",
            created_at=datetime.now(timezone.utc),
        )
        db.add(organization)
        db.flush()

    workspace = db.get(Workspace, DEFAULT_WORKSPACE_ID)
    if workspace is None:
        workspace = Workspace(
            id=DEFAULT_WORKSPACE_ID,
            organization_id=organization.id,
            name="Threat Research Workspace",
            slug="threat-research",
            created_at=datetime.now(timezone.utc),
        )
        db.add(workspace)
        db.flush()

    return organization, workspace


def ensure_user_for_principal(principal: CurrentPrincipal, db: Session) -> User:
    """Materialize a lightweight user row for token-only scaffold principals when needed."""
    _ensure_auth_tables()
    user = _get_user_with_memberships(db, user_id=principal.subject)
    if user is None:
        user = _get_user_with_memberships(db, email=principal.email)
    if user is not None:
        return user

    user = User(
        id=principal.subject,
        display_name=_build_display_name(principal.email),
        email=principal.email,
        password_hash=_hash_password(get_settings().demo_org_admin_password),
        platform_role=principal.role,
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.flush()
    return user


def _attach_default_memberships(db: Session, user: User, account_type: str) -> tuple[str | None, str | None]:
    """Create the minimal scaffold membership structure for a newly registered user."""
    if account_type == "organization":
        organization = Organization(
            name=f"{user.display_name} Organization",
            slug=f"{user.display_name.lower().replace(' ', '-')}-{user.id[:8]}",
            created_at=datetime.now(timezone.utc),
        )
        db.add(organization)
        db.flush()

        workspace = Workspace(
            organization_id=organization.id,
            name="Primary Workspace",
            slug="primary-workspace",
            created_at=datetime.now(timezone.utc),
        )
        db.add(workspace)
        db.flush()

        db.add(
            Membership(
                user_id=user.id,
                organization_id=organization.id,
                workspace_id=workspace.id,
                role="org_owner",
                created_at=datetime.now(timezone.utc),
            )
        )
        user.platform_role = "org_owner"
        return organization.id, workspace.id

    organization, workspace = _get_or_create_demo_org_and_workspace(db)
    db.add(
        Membership(
            user_id=user.id,
            organization_id=organization.id,
            workspace_id=workspace.id,
            role="analyst",
            created_at=datetime.now(timezone.utc),
        )
    )
    user.platform_role = "analyst"
    return organization.id, workspace.id


def _token_for_user(user: User) -> TokenResponse:
    """Create the bearer token returned to DB-backed users."""
    memberships = list(user.memberships)
    primary_membership = memberships[0] if memberships else None
    role = choose_higher_role(user.platform_role, *(membership.role for membership in memberships))
    organization_id = primary_membership.organization_id if primary_membership else None
    workspace_id = primary_membership.workspace_id if primary_membership else None
    token = create_access_token(
        {
            "sub": user.id,
            "email": user.email,
            "role": role,
            "organization_id": organization_id,
            "workspace_id": workspace_id,
        }
    )
    return TokenResponse(
        access_token=token,
        principal_role=role,
        organization_id=organization_id,
        workspace_id=workspace_id,
    )


def _login_demo_user(payload: LoginRequest) -> TokenResponse:
    """Authenticate one of the deterministic scaffold demo users."""
    settings = get_settings()
    role = "analyst"
    password_ok = payload.password == settings.demo_org_admin_password
    if payload.password == settings.demo_platform_admin_password:
        role = "platform_admin"
        password_ok = True
    elif payload.email.startswith("owner@"):
        role = "org_owner"
    elif payload.email.startswith("admin@"):
        role = "org_admin"

    if not password_ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    token = create_access_token(
        {
            "sub": payload.email,
            "email": payload.email,
            "role": role,
            "organization_id": DEFAULT_ORGANIZATION_ID,
            "workspace_id": DEFAULT_WORKSPACE_ID,
        }
    )
    return TokenResponse(
        access_token=token,
        principal_role=role,
        organization_id=DEFAULT_ORGANIZATION_ID,
        workspace_id=DEFAULT_WORKSPACE_ID,
    )


def get_user_profile_for_principal(principal: CurrentPrincipal, db: Session) -> UserProfileResponse:
    """Resolve the current principal into a DB-backed or deterministic scaffold profile."""
    _ensure_auth_tables()
    user = _get_user_with_memberships(db, user_id=principal.subject)
    if user is None:
        user = _get_user_with_memberships(db, email=principal.email)
    if user is not None:
        return _serialize_user_profile(user)

    return UserProfileResponse(
        id=principal.subject,
        display_name=_build_display_name(principal.email),
        email=principal.email,
        platform_role=principal.role,
        memberships=[
            MembershipSummary(
                organization_id=principal.organization_id or DEFAULT_ORGANIZATION_ID,
                workspace_id=principal.workspace_id or DEFAULT_WORKSPACE_ID,
                role=principal.role,
            )
        ],
        created_at=datetime.now(timezone.utc),
    )


def get_memberships_for_principal(principal: CurrentPrincipal, db: Session) -> list[MembershipSummary]:
    """Expose membership lookup for other route modules without duplicating auth logic."""
    return get_user_profile_for_principal(principal, db).memberships


@router.post("/register", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
) -> UserProfileResponse:
    """Register a user and create the minimal membership scaffold in the database."""
    _ensure_auth_tables()
    existing_user = _get_user_with_memberships(db, email=payload.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        display_name=payload.display_name,
        email=payload.email,
        password_hash=_hash_password(payload.password),
        platform_role="analyst",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.flush()
    _attach_default_memberships(db, user, payload.account_type)
    db.commit()
    user = _get_user_with_memberships(db, user_id=user.id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registered user could not be reloaded.",
        )
    return _serialize_user_profile(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Return a bearer token for DB-backed users or deterministic demo accounts."""
    _ensure_auth_tables()
    user = _get_user_with_memberships(db, email=payload.email)
    if user is not None:
        if not user.is_active or not _verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )
        return _token_for_user(user)
    return _login_demo_user(payload)


@router.get("/me", response_model=UserProfileResponse)
async def me(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> UserProfileResponse:
    """Return the current user profile."""
    return get_user_profile_for_principal(principal, db)
