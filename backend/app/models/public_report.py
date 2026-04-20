"""
Purpose:
    Public-safe report model for the anonymized public threats layer.
Inputs:
    Sanitized publish requests or approved external uploads.
Outputs:
    Public feed entries with no direct organization/workspace linkage.
Dependencies:
    SQLAlchemy Base and model column types.
TODO Checklist:
    - [ ] Revisit storage separation if the team decides to use a distinct public database.
    - [ ] Add taxonomy/tag fields once public filtering is implemented.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PublicReport(Base):
    """
    Public threat report.

    Critical rule:
        This table intentionally avoids direct foreign keys back to users,
        organizations, workspaces, or private report IDs.
    """

    __tablename__ = "public_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    public_slug: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(180))
    summary: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(16), default="medium")
    indicator_count: Mapped[int] = mapped_column(default=0)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    source_kind: Mapped[str] = mapped_column(String(32), default="workspace_publish")
    status: Mapped[str] = mapped_column(String(32), default="published", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
