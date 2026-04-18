"""
Purpose:
    User-oriented account endpoints beyond raw authentication.
Inputs:
    Current principal context and membership assignment payloads.
Outputs:
    User profile and membership views for frontend account pages.
Dependencies:
    Auth route helpers, SQLAlchemy models, and user schemas.
TODO Checklist:
    - [ ] Add profile update endpoint only if it becomes part of project scope.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_principal
from app.api.routes.auth import _ensure_auth_tables, get_memberships_for_principal, get_user_profile_for_principal
from app.core.permissions import can_manage_organization
from app.db.session import get_db
from app.models import Membership, Organization, User, Workspace
from app.schemas.auth import CurrentPrincipal
from app.schemas.user import (
    MembershipAssignmentRequest,
    MembershipSummary,
    UserProfileResponse,
    UserSummaryResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


def _get_user(db: Session, user_id: str) -> User | None:
    """Load one user with memberships for user-scoped endpoints."""
    return db.scalar(
        select(User)
        .options(selectinload(User.memberships))
        .where(User.id == user_id)
    )


@router.get("/me", response_model=UserProfileResponse)
async def get_me(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> UserProfileResponse:
    """Return the current DB-backed profile when available."""
    return get_user_profile_for_principal(principal, db)


@router.get("/me/memberships", response_model=list[MembershipSummary])
async def get_my_memberships(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> list[MembershipSummary]:
    """Return memberships for the current user."""
    return get_memberships_for_principal(principal, db)


@router.get("/{user_id}", response_model=UserSummaryResponse)
async def get_user(
    user_id: str,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> UserSummaryResponse:
    """Return a compact user summary within the caller's organization scope."""
    _ensure_auth_tables()
    user = _get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    principal_org_ids = {membership.organization_id for membership in get_memberships_for_principal(principal, db)}
    user_org_ids = {membership.organization_id for membership in user.memberships}
    if principal.role != "platform_admin" and principal_org_ids.isdisjoint(user_org_ids):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is outside the current organization scope.",
        )

    return UserSummaryResponse(
        id=user.id,
        display_name=user.display_name,
        email=user.email,
        platform_role=user.platform_role,
    )


@router.post("/memberships", response_model=MembershipSummary, status_code=status.HTTP_201_CREATED)
async def assign_membership(
    payload: MembershipAssignmentRequest,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> MembershipSummary:
    """Assign a user to an organization or workspace using simple scaffold RBAC."""
    _ensure_auth_tables()
    if not can_manage_organization(principal.role) and principal.role != "platform_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization management privileges are required.",
        )

    user = db.get(User, payload.user_id)
    organization = db.get(Organization, payload.organization_id)
    workspace = db.get(Workspace, payload.workspace_id) if payload.workspace_id else None
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")
    if workspace is not None and workspace.organization_id != organization.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace does not belong to the target organization.",
        )

    existing_membership = db.scalar(
        select(Membership).where(
            Membership.user_id == payload.user_id,
            Membership.organization_id == payload.organization_id,
            Membership.workspace_id == payload.workspace_id,
        )
    )
    if existing_membership is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This membership already exists.",
        )

    membership = Membership(
        user_id=payload.user_id,
        organization_id=payload.organization_id,
        workspace_id=payload.workspace_id,
        role=payload.role,
    )
    db.add(membership)
    db.commit()

    if principal.role == "platform_admin" or payload.role in {"org_owner", "org_admin"}:
        user.platform_role = payload.role
        db.add(user)
        db.commit()

    return MembershipSummary(
        organization_id=membership.organization_id,
        workspace_id=membership.workspace_id,
        role=membership.role,
    )
