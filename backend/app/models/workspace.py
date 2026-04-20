"""
Purpose:
    Workspace model for scoping artifacts, reports, and dashboard views inside an organization.
Inputs:
    Workspace management flows and future role-based authorization checks.
Outputs:
    Private workspace rows tied to an organization.
Dependencies:
    SQLAlchemy Base and model column types.
TODO Checklist:
    - [ ] Add workspace retention/policy fields once private/public sharing rules are finalized.
    - [ ] Add soft-delete/archive support if the team needs demo cleanup flows.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Workspace(Base):
    """Workspace within an organization."""

    __tablename__ = "workspaces"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_workspaces_org_slug"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(160), index=True)
    organization: Mapped["Organization"] = relationship("Organization", back_populates="workspaces")
    memberships: Mapped[list["Membership"]] = relationship(
        "Membership",
        back_populates="workspace",
        cascade="save-update, merge",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
