"""
Purpose:
    Private threat report model produced from scan orchestration and enrichment.
Inputs:
    Completed scan jobs, enrichment results, and optional AI analysis.
Outputs:
    Workspace-scoped threat reports for dashboard and sharing flows.
Dependencies:
    SQLAlchemy Base and model column types.
TODO Checklist:
    - [ ] Split report sections into child tables only if editing/versioning becomes necessary.
    - [ ] Add analyst annotation support in a later phase if the team needs collaboration.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ThreatReport(Base):
    """Workspace-scoped private report generated for a scan job."""

    __tablename__ = "threat_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    scan_job_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    workspace_id: Mapped[str] = mapped_column(String(64), index=True)
    severity: Mapped[str] = mapped_column(String(16), default="medium")
    confidence: Mapped[int] = mapped_column(default=50)
    executive_summary: Mapped[str] = mapped_column(Text)
    recommended_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    source_summary: Mapped[list[str]] = mapped_column(JSON, default=list)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    publish_status: Mapped[str] = mapped_column(String(32), default="private")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
