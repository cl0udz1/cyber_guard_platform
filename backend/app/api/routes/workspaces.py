"""
Purpose:
    Workspace management endpoints for organization-scoped analysis areas.
Inputs:
    Workspace payloads and authenticated principal context.
Outputs:
    Workspace summaries and list responses.
Dependencies:
    Workspace schemas, auth dependencies, SQLAlchemy models, and permission helpers.
TODO Checklist:
    - [ ] Add archive/delete flows only if they become necessary for the team.
    - [ ] Add explicit workspace switching if the frontend needs it later.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_principal
from app.api.routes.auth import _ensure_auth_tables, ensure_user_for_principal
from app.api.routes.orgs import organization_exists_for_principal
from app.core.permissions import can_access_workspace, can_manage_workspace
from app.db.session import get_db
from app.models import Membership, Workspace
from app.schemas.auth import CurrentPrincipal
from app.schemas.workspace import WorkspaceCreateRequest, WorkspaceResponse
from app.utils.constants import DEFAULT_ORGANIZATION_ID, DEFAULT_WORKSPACE_ID

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


def _workspace_membership_count(db: Session, workspace_id: str) -> int:
    """Return how many memberships point to a given workspace."""
    return db.scalar(select(func.count(Membership.id)).where(Membership.workspace_id == workspace_id)) or 0


def _serialize_workspace(db: Session, workspace: Workspace) -> WorkspaceResponse:
    """Convert one workspace row into the public response shape."""
    return WorkspaceResponse(
        id=workspace.id,
        organization_id=workspace.organization_id,
        name=workspace.name,
        slug=workspace.slug,
        created_at=workspace.created_at,
        membership_count=_workspace_membership_count(db, workspace.id),
    )


def _seed_default_workspace(principal: CurrentPrincipal) -> WorkspaceResponse:
    """Create the deterministic workspace returned by the scaffold by default."""
    return WorkspaceResponse(
        id=principal.workspace_id or DEFAULT_WORKSPACE_ID,
        organization_id=principal.organization_id or DEFAULT_ORGANIZATION_ID,
        name="Threat Research Workspace",
        slug="threat-research",
        created_at=datetime.now(timezone.utc),
        membership_count=1,
    )


def _list_visible_workspaces(principal: CurrentPrincipal, db: Session) -> list[WorkspaceResponse]:
    """Return DB-backed workspaces inside the visible organization scope."""
    _ensure_auth_tables()
    statement = select(Workspace).order_by(Workspace.created_at, Workspace.name)
    if principal.role == "platform_admin":
        workspaces = list(db.scalars(statement))
    elif can_manage_workspace(principal.role):
        statement = statement.where(Workspace.organization_id == (principal.organization_id or DEFAULT_ORGANIZATION_ID))
        workspaces = list(db.scalars(statement))
    else:
        workspaces = list(
            db.scalars(
                statement
                .join(Membership, Membership.workspace_id == Workspace.id)
                .where(Membership.user_id == principal.subject)
            )
        )
    if not workspaces and principal.workspace_id == DEFAULT_WORKSPACE_ID:
        return [_seed_default_workspace(principal)]
    return [_serialize_workspace(db, workspace) for workspace in workspaces]


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    payload: WorkspaceCreateRequest,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> WorkspaceResponse:
    """Create a workspace inside the caller's visible organization scope."""
    _ensure_auth_tables()
    if not can_manage_workspace(principal.role) and principal.role != "platform_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Org owners or org admins are required to create workspaces.",
        )
    if not organization_exists_for_principal(principal, db, payload.organization_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found for workspace creation.",
        )
    existing_workspace = db.scalar(
        select(Workspace).where(
            Workspace.organization_id == payload.organization_id,
            Workspace.slug == payload.slug,
        )
    )
    if existing_workspace is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A workspace with this slug already exists in the organization.",
        )

    workspace = Workspace(
        organization_id=payload.organization_id,
        name=payload.name,
        slug=payload.slug,
        created_at=datetime.now(timezone.utc),
    )
    db.add(workspace)
    db.flush()
    principal_user = ensure_user_for_principal(principal, db)
    db.add(
        Membership(
            user_id=principal_user.id,
            organization_id=payload.organization_id,
            workspace_id=workspace.id,
            role=principal.role if principal.role in {"org_owner", "org_admin"} else "org_admin",
            created_at=datetime.now(timezone.utc),
        )
    )
    db.commit()
    db.refresh(workspace)
    return _serialize_workspace(db, workspace)


@router.get("", response_model=list[WorkspaceResponse])
async def list_workspaces(
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> list[WorkspaceResponse]:
    """Return workspace list for the current principal."""
    return _list_visible_workspaces(principal, db)


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    principal: CurrentPrincipal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> WorkspaceResponse:
    """Return a single workspace summary when it is visible to the current principal."""
    _ensure_auth_tables()
    workspace = db.get(Workspace, workspace_id)
    if workspace is not None:
        if not can_access_workspace(
            principal.role,
            principal.organization_id,
            workspace.organization_id,
            principal.workspace_id,
            workspace.id,
        ):
            principal_membership = db.scalar(
                select(Membership.id).where(
                    Membership.user_id == principal.subject,
                    Membership.workspace_id == workspace.id,
                )
            )
            if principal_membership is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Workspace is outside the current principal scope.",
                )
        return _serialize_workspace(db, workspace)

    seeded_workspace = _seed_default_workspace(principal)
    if workspace_id == seeded_workspace.id:
        return seeded_workspace

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Workspace not found for the current principal.",
    )
