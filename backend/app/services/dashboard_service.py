"""
Purpose:
    Build workspace dashboard overview responses from scan/report activity.
Inputs:
    Workspace scope plus future DB aggregates.
Outputs:
    Typed dashboard summary payloads for the frontend.
Dependencies:
    Dashboard schemas.
TODO Checklist:
    - [ ] Replace placeholder metrics with DB aggregates.
    - [ ] Add time-range filtering and charts once the frontend needs real series data.
"""

from collections import Counter
from collections.abc import Callable
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.admin_review import AdminReview
from app.models.public_report import PublicReport
from app.models.threat_report import ThreatReport
from app.schemas.dashboard import DashboardMetric, DashboardOverviewResponse
from app.utils.constants import DEFAULT_WORKSPACE_ID
from app.utils.enums import PublicShareStatus


_tables_ready = False


def _ensure_dashboard_tables() -> None:
    """Create dashboard-related tables on first use for scaffold persistence."""
    global _tables_ready
    if _tables_ready:
        return
    Base.metadata.create_all(bind=engine)
    _tables_ready = True


def _extract_source_name(summary: str) -> str:
    """Infer a compact source label from report source summary text."""
    source_name = summary.strip().split(" ", maxsplit=1)[0].strip(":,.;").lower()
    return source_name or "unknown"


class DashboardService:
    """Return high-level workspace metrics suitable for scaffold demos."""

    def __init__(self, session_factory: Callable[[], Session] = SessionLocal) -> None:
        self._session_factory = session_factory

    def build_overview(
        self,
        workspace_id: str = DEFAULT_WORKSPACE_ID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> DashboardOverviewResponse:
        """Return high-level workspace metrics from persisted scaffold data."""
        _ensure_dashboard_tables()

        report_filters = [ThreatReport.workspace_id == workspace_id]
        if start_date is not None:
            report_filters.append(ThreatReport.created_at >= start_date)
        if end_date is not None:
            report_filters.append(ThreatReport.created_at <= end_date)

        with self._session_factory() as db:
            report_count = db.scalar(
                select(func.count(ThreatReport.id)).where(*report_filters)
            ) or 0
            queued_publish_count = db.scalar(
                select(func.count(AdminReview.id)).where(AdminReview.status == "pending")
            ) or 0
            published_public_count = db.scalar(
                select(func.count(PublicReport.id)).where(
                    PublicReport.status == PublicShareStatus.PUBLISHED.value
                )
            ) or 0
            report_rows = db.scalars(
                select(ThreatReport.source_summary).where(*report_filters)
            ).all()

        source_counter: Counter[str] = Counter()
        for source_list in report_rows:
            for source_summary in source_list or []:
                source_counter[_extract_source_name(source_summary)] += 1

        top_sources = [source for source, _count in source_counter.most_common(3)]
        if not top_sources:
            top_sources = ["virustotal", "source_a", "source_b"]

        return DashboardOverviewResponse(
            workspace_id=workspace_id,
            metrics=[
                DashboardMetric(
                    label="Queued Jobs",
                    value=str(queued_publish_count),
                    note="Review items waiting for a moderation decision.",
                ),
                DashboardMetric(
                    label="Reports Ready",
                    value=str(report_count),
                    note="Private reports available to analysts.",
                ),
                DashboardMetric(
                    label="Public Posts",
                    value=str(published_public_count),
                    note="Approved anonymized reports in public feed.",
                ),
            ],
            recent_scan_statuses={"completed": report_count, "enriching": 0, "queued": 0},
            publish_queue_count=queued_publish_count,
            top_sources=top_sources,
        )
