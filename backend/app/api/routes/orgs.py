"""
Purpose:
    Organization management endpoints for the scaffold contract.
Inputs:
    Organization payloads and authenticated principal context.
Outputs:
    Organization summaries and membership listings.
Dependencies:
    Auth dependencies, org schemas, SQLAlchemy models, and permission helpers.
TODO Checklist:
    - [ ] Add invitation endpoints after workspace/membership work is in place.
    - [ ] Add organization settings after governance fields are defined.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_principal
from app.api.routes.auth import _ensure_auth_tables, ensure_user_for_principal
from app.core.permissions import can_access_organization, can_manage_organization
from app.db.session import get_db
from app.models import Membership, Organization
from app.schemas.auth import CurrentPrincipal
from app.schemas.org import MembershipResponse, OrganizationCreateRequest, OrganizationResponse
from app.utils.constants import DEFAULT_ORGANIZATION_ID, DEFAULT_WORKSPACE_ID

router = APIRouter(prefix="/orgs", tags=["organizations"])


def _serialize_organization(db: Session, organization: Organization) -> OrganizationResponse:
    """Convert one organization row into the public response shape."""
    membership_count = db.scalar(
        select(func.count(Membership.id)).where(Membership.organization_id == organization.id)
    )
    return OrganizationResponse(
        id=organization.id,
        name=organization.name,
        slug=organization.slug,
        sector=organization.sector,
        created_at=organization.created_at,
        membership_count=membership_count or 0,
    )


def _seed_demo_organization(db: Session) -> Organization:
    """Keep the deterministic demo organization available for scaffold flows."""
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
        db.commit()
        db.refresh(organization)
    return organization


def _membership_rows_for_org(db: Session, org_id: str) -> list[Membership]:
    """Load memberships for one organization in a stable order."""
    return list(
        db.scalars(
            select(Membership)
            .where(Membership.organization_id == org_id)
            .order_by(Membership.created_at, Membership.user_id)
        )
    )


def _principal_has_membership(principal: CurrentPrincipal, db: Session, org_id: str) -> bool:
    """Check whether the current caller belongs to the target organization."""
    return (
        db.scalar(
            select(Membership.id).where(
                Membership.organization_id == org_id,
                Membership.user_id == principal.subject,
            )
        )
        is not None
    )


def get_visible_organization(principal: CurrentPrincipal, db: Session, org_id: str) -> Organization:
    """Return an organization row when the caller is allowed to see it."""
    _ensure_auth_tables()
    organization = db.get(Organization, org_id)
    if organization is None and org_id == DEFAULT_ORGANIZATION_ID:
        organization = _seed_demo_organization(db)
    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found for the current principal.",
        )
    if can_access_organization(principal.role, principal.organization_id, org_id) or _principal_has_membership(
        principal,
        db,
        org_id,
    ):
        return organization
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Organization is outside the current principal scope.",
    )


def organization_exists_for_principal(principal: CurrentPrincipal, db: Session, org_id: str) -> bool:
    """Expose a safe org-existence check for workspace routes."""
    try:
        get_visible_organization(principal, db, org_id)
    except HTTPException:
        return False
    return True


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_org(
    payload: OrganizationCreateRequest,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    """Create an organization and attach the creator as org owner."""
    _ensure_auth_tables()
    caller_membership_count = db.scalar(select(func.count(Membership.id)).where(Membership.user_id == principal.subject)) or 0
    if caller_membership_count > 0 and not can_manage_organization(principal.role) and principal.role != "platform_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization management privileges are required to create another organization.",
        )

    existing_org = db.scalar(select(Organization).where(Organization.slug == payload.slug))
    if existing_org is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An organization with this slug already exists.",
        )

    principal_user = ensure_user_for_principal(principal, db)

    organization = Organization(
        name=payload.name,
        slug=payload.slug,
        sector=payload.sector,
        created_at=datetime.now(timezone.utc),
    )
    db.add(organization)
    db.flush()

    existing_owner_membership = db.scalar(
        select(Membership).where(
            Membership.user_id == principal_user.id,
            Membership.organization_id == organization.id,
            Membership.workspace_id.is_(None),
        )
    )
    if existing_owner_membership is None:
        db.add(
            Membership(
                user_id=principal_user.id,
                organization_id=organization.id,
                workspace_id=None,
                role="org_owner",
                created_at=datetime.now(timezone.utc),
            )
        )

    db.commit()
    db.refresh(organization)
    return _serialize_organization(db, organization)


@router.get("", response_model=list[OrganizationResponse])
async def list_orgs(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> list[OrganizationResponse]:
    """Return organizations visible to the current principal."""
    _ensure_auth_tables()
    if principal.role == "platform_admin":
        organizations = list(db.scalars(select(Organization).order_by(Organization.created_at, Organization.name)))
        return [_serialize_organization(db, organization) for organization in organizations]

    organizations = list(
        db.scalars(
            select(Organization)
            .join(Membership, Membership.organization_id == Organization.id)
            .where(Membership.user_id == principal.subject)
            .distinct()
            .order_by(Organization.created_at, Organization.name)
        )
    )
    if not organizations and principal.organization_id == DEFAULT_ORGANIZATION_ID:
        organizations = [_seed_demo_organization(db)]
    return [_serialize_organization(db, organization) for organization in organizations]


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_org(
    org_id: str,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> OrganizationResponse:
    """Return an organization summary when it is visible to the current principal."""
    organization = get_visible_organization(principal, db, org_id)
    return _serialize_organization(db, organization)


@router.get("/{org_id}/memberships", response_model=list[MembershipResponse])
async def get_org_memberships(
    org_id: str,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> list[MembershipResponse]:
    """Return stored memberships for an organization the caller can access."""
    get_visible_organization(principal, db, org_id)
    memberships = _membership_rows_for_org(db, org_id)
    if memberships:
        return [
            MembershipResponse(
                user_id=membership.user_id,
                workspace_id=membership.workspace_id,
                role=membership.role,
            )
            for membership in memberships
        ]

    return [
        MembershipResponse(
            user_id=principal.subject,
            workspace_id=principal.workspace_id or DEFAULT_WORKSPACE_ID,
            role=principal.role,
        )
    ]
