"""
Purpose:
    Private identity model for Cyber Guard accounts.
Inputs:
    Account creation, login, and organization membership workflows.
Outputs:
    Persisted user rows for future DB-backed authentication.
Dependencies:
    SQLAlchemy Base and model column types.
TODO Checklist:
    - [ ] Add email verification and invitation acceptance metadata.
    - [ ] Add audit fields for last login and password reset events.
    - [ ] Keep public-sharing data disconnected from this identity table.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    """Private user account table used for authenticated experiences."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=lambda: str(uuid4()))
    display_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    platform_role: Mapped[str] = mapped_column(String(32), default="analyst")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    memberships: Mapped[list["Membership"]] = relationship(
        "Membership",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
