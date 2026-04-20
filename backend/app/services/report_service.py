"""
Purpose:
    Build and store private threat report placeholders from completed scan jobs.
Inputs:
    Scan job metadata, enrichment hits, and optional AI summary text.
Outputs:
    Typed threat report responses retrievable by report ID.
Dependencies:
    Report schemas and threat severity rules.
TODO Checklist:
    - [ ] Replace in-memory storage with DB persistence.
    - [ ] Add section versioning only if analyst editing becomes part of scope.
"""

from datetime import datetime, timezone
from collections.abc import Callable
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.threat_report import ThreatReport
from app.schemas.artifact import ArtifactSubmissionResponse
from app.schemas.report import ThreatReportResponse
from app.schemas.scan import SourceHit
from app.utils.enums import PublicShareStatus, ThreatSeverity


_tables_ready = False


def _ensure_report_tables() -> None:
    """Create report-related tables on first use for scaffold persistence."""
    global _tables_ready
    if _tables_ready:
        return
    Base.metadata.create_all(bind=engine)
    _tables_ready = True


def _to_threat_report_response(model: ThreatReport) -> ThreatReportResponse:
    """Convert ORM report row to API schema."""
    severity = ThreatSeverity.MEDIUM
    try:
        severity = ThreatSeverity(model.severity)
    except ValueError:
        pass

    publish_status = PublicShareStatus.PRIVATE
    try:
        publish_status = PublicShareStatus(model.publish_status)
    except ValueError:
        pass

    return ThreatReportResponse(
        report_id=model.id,
        scan_job_id=model.scan_job_id,
        severity=severity,
        confidence=model.confidence,
        executive_summary=model.executive_summary,
        recommended_actions=model.recommended_actions or [],
        source_summary=model.source_summary or [],
        ai_summary=model.ai_summary,
        publish_status=publish_status,
        created_at=model.created_at,
    )


class ReportService:
    """Create and retrieve scaffold threat reports with lightweight persistence."""

    def __init__(self, session_factory: Callable[[], Session] = SessionLocal) -> None:
        self._session_factory = session_factory

    async def build_report(
        self,
        scan_job_id: str,
        artifact: ArtifactSubmissionResponse,
        source_hits: list[SourceHit],
        ai_summary: str | None,
    ) -> ThreatReportResponse:
        """Build a private threat report from source hits and optional AI output."""
        max_score = max((hit.confidence_score for hit in source_hits), default=20)
        severity = ThreatSeverity.MEDIUM
        if max_score >= 80:
            severity = ThreatSeverity.HIGH
        elif max_score < 35:
            severity = ThreatSeverity.LOW

        report_row = ThreatReport(
            id=str(uuid4()),
            scan_job_id=scan_job_id,
            workspace_id=artifact.workspace_id,
            severity=severity.value,
            confidence=max_score,
            executive_summary=f"Scaffold report for {artifact.artifact_type.value} artifact submission.",
            recommended_actions=[
                "Review source findings in the private workspace.",
                "Decide whether anonymized publication is appropriate.",
                "Track duplicate submissions before escalating externally.",
            ],
            source_summary=[hit.summary for hit in source_hits],
            ai_summary=ai_summary,
            publish_status=PublicShareStatus.PRIVATE.value,
            created_at=datetime.now(timezone.utc),
        )

        _ensure_report_tables()
        with self._session_factory() as db:
            db.add(report_row)
            db.commit()
            db.refresh(report_row)

        return _to_threat_report_response(report_row)

    def get_report(
        self,
        report_id: str,
        workspace_id: str | None = None,
    ) -> ThreatReportResponse | None:
        """Return a previously built report if it exists in scope."""
        _ensure_report_tables()
        with self._session_factory() as db:
            statement = select(ThreatReport).where(ThreatReport.id == report_id)
            if workspace_id is not None:
                statement = statement.where(ThreatReport.workspace_id == workspace_id)
            model = db.scalar(statement)

        if model is None:
            return None

        return _to_threat_report_response(model)

    def set_publish_status(self, report_id: str, status: PublicShareStatus) -> bool:
        """Persist report publication status updates for sharing workflows."""
        _ensure_report_tables()
        with self._session_factory() as db:
            model = db.get(ThreatReport, report_id)
            if model is None:
                return False
            model.publish_status = status.value
            db.add(model)
            db.commit()
        return True
