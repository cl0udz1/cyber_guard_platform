"""
Purpose:
    Membership model for user access to organizations and optionally specific workspaces.
Inputs:
    Invitation, join, and role management workflows.
Outputs:
    Private role assignment rows for RBAC enforcement.
Dependencies:
    SQLAlchemy Base and model column types.
TODO Checklist:
    - [ ] Add invitation status and expiration fields for real onboarding.
    - [ ] Clarify whether workspace-specific memberships need a separate table later.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Membership(Base):
    """Role assignment connecting users to organizations/workspaces."""

    __tablename__ = "memberships"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "organization_id",
            "workspace_id",
            name="uq_memberships_user_org_workspace",
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    workspace_id: Mapped[str | None] = mapped_column(ForeignKey("workspaces.id"), nullable=True)
    role: Mapped[str] = mapped_column(String(32), default="analyst")
    user: Mapped["User"] = relationship("User", back_populates="memberships")
    organization: Mapped["Organization"] = relationship("Organization", back_populates="memberships")
    workspace: Mapped["Workspace | None"] = relationship("Workspace", back_populates="memberships")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
