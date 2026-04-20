"""
Purpose:
    Prepare anonymized public threat outputs from private reports or external uploads.
Inputs:
    Private report details, publish requests, and external report metadata.
Outputs:
    Public-safe summaries and publication workflow status.
Dependencies:
    Sanitization service and public threat schemas.
TODO Checklist:
    - [ ] Add stronger anonymization checks before production use.
    - [ ] Add DB persistence and public slug uniqueness rules.
"""

from datetime import datetime, timezone
from collections.abc import Callable
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.public_report import PublicReport
from app.schemas.public_threats import PublicThreatListResponse, PublicThreatSummary
from app.schemas.report import ExternalReportUploadRequest, PublishRequest, ThreatReportResponse
from app.services.sanitization_service import SanitizationService
from app.utils.enums import PublicShareStatus, ThreatSeverity


_tables_ready = False


def _ensure_public_sharing_tables() -> None:
    """Create public-sharing tables on first use for scaffold persistence."""
    global _tables_ready
    if _tables_ready:
        return
    Base.metadata.create_all(bind=engine)
    _tables_ready = True


def _to_public_summary(report_row: PublicReport) -> PublicThreatSummary:
    """Convert ORM public report row to public threat schema."""
    severity = ThreatSeverity.MEDIUM
    try:
        severity = ThreatSeverity(report_row.severity)
    except ValueError:
        pass

    published_at = report_row.approved_at or report_row.created_at
    return PublicThreatSummary(
        public_report_id=report_row.id,
        public_slug=report_row.public_slug,
        title=report_row.title,
        summary=report_row.summary,
        severity=severity,
        indicator_count=report_row.indicator_count,
        source_kind=report_row.source_kind,
        published_at=published_at,
    )


class PublicSharingService:
    """Scaffold service for anonymized sharing workflows."""

    def __init__(
        self,
        sanitization_service: SanitizationService,
        admin_review_required: bool,
        session_factory: Callable[[], Session] = SessionLocal,
    ) -> None:
        self.sanitization_service = sanitization_service
        self.admin_review_required = admin_review_required
        self._session_factory = session_factory

    def create_publish_request(
        self,
        report: ThreatReportResponse,
        payload: PublishRequest,
    ) -> dict[str, object]:
        """Return a scaffold publish request preview."""
        public_summary = self.sanitization_service.sanitize_summary(report.executive_summary)
        public_payload = {
            "title": f"Anonymized threat report {report.report_id[:8]}",
            "summary": public_summary,
            "severity": report.severity.value,
            "indicator_count": len(report.source_summary),
            "notes_for_reviewer": payload.notes_for_reviewer,
        }
        self.sanitization_service.assert_identity_safe(public_payload)

        _ensure_public_sharing_tables()
        status = (
            PublicShareStatus.PENDING_REVIEW.value
            if self.admin_review_required
            else PublicShareStatus.PUBLISHED.value
        )
        now = datetime.now(timezone.utc)
        public_report_row = PublicReport(
            id=str(uuid4()),
            public_slug=f"threat-{uuid4().hex[:10]}",
            title=str(public_payload["title"]),
            summary=str(public_payload["summary"]),
            severity=str(public_payload["severity"]),
            indicator_count=int(public_payload["indicator_count"]),
            source_kind="workspace_publish",
            status=status,
            created_at=now,
            approved_at=now if status == PublicShareStatus.PUBLISHED.value else None,
        )
        with self._session_factory() as db:
            db.add(public_report_row)
            db.commit()
            db.refresh(public_report_row)

        return {
            "report_id": report.report_id,
            "status": "pending_review" if self.admin_review_required else "publish_ready",
            "public_payload_preview": public_payload,
            "public_report_id": public_report_row.id,
        }

    def accept_external_upload(self, payload: ExternalReportUploadRequest) -> dict[str, object]:
        """Return scaffold metadata for an external upload review request."""
        _ensure_public_sharing_tables()
        sanitized_summary = self.sanitization_service.sanitize_summary(payload.summary)
        public_payload = {
            "title": payload.title,
            "summary": sanitized_summary,
            "severity": ThreatSeverity.MEDIUM.value,
            "indicator_count": 0,
            "source_kind": "external_upload",
        }
        self.sanitization_service.assert_identity_safe(public_payload)

        public_report_row = PublicReport(
            id=str(uuid4()),
            public_slug=f"threat-{uuid4().hex[:10]}",
            title=payload.title,
            summary=sanitized_summary,
            severity=ThreatSeverity.MEDIUM.value,
            indicator_count=0,
            source_kind="external_upload",
            status=PublicShareStatus.PENDING_REVIEW.value,
            created_at=datetime.now(timezone.utc),
            approved_at=None,
        )
        with self._session_factory() as db:
            db.add(public_report_row)
            db.commit()
            db.refresh(public_report_row)

        return {
            "upload_reference": public_report_row.id,
            "status": "pending_review",
            "title": payload.title,
        }

    def publish_public_report(self, title: str, summary: str, severity: ThreatSeverity) -> PublicThreatSummary:
        """Create a public-safe feed entry with no private link fields."""
        _ensure_public_sharing_tables()
        now = datetime.now(timezone.utc)
        public_report_row = PublicReport(
            id=str(uuid4()),
            public_slug=f"threat-{uuid4().hex[:10]}",
            title=title,
            summary=self.sanitization_service.sanitize_summary(summary),
            severity=severity.value,
            indicator_count=3,
            source_kind="workspace_publish",
            status=PublicShareStatus.PUBLISHED.value,
            created_at=now,
            approved_at=now,
        )
        with self._session_factory() as db:
            db.add(public_report_row)
            db.commit()
            db.refresh(public_report_row)

        return _to_public_summary(public_report_row)

    def apply_review_decision(
        self,
        review_type: str,
        submission_reference: str,
        decision: str,
    ) -> None:
        """Apply moderation decisions to pending public reports."""
        if review_type not in {"report_publish_request", "external_report_upload"}:
            return

        _ensure_public_sharing_tables()
        with self._session_factory() as db:
            report_row = db.get(PublicReport, submission_reference)
            if report_row is None:
                return

            if decision == "approve":
                report_row.status = PublicShareStatus.PUBLISHED.value
                report_row.approved_at = datetime.now(timezone.utc)
            elif decision == "reject":
                report_row.status = PublicShareStatus.REJECTED.value
            else:
                report_row.status = PublicShareStatus.PENDING_REVIEW.value

            db.add(report_row)
            db.commit()

    def list_public_reports(
        self,
        limit: int = 20,
        cursor: str | None = None,
        severity: ThreatSeverity | None = None,
    ) -> PublicThreatListResponse:
        """Return the current public feed placeholder items."""
        _ensure_public_sharing_tables()

        with self._session_factory() as db:
            statement = select(PublicReport).where(
                PublicReport.status == PublicShareStatus.PUBLISHED.value
            )
            if severity is not None:
                statement = statement.where(PublicReport.severity == severity.value)
            published_rows = db.scalars(
                statement.order_by(PublicReport.approved_at.desc(), PublicReport.created_at.desc())
            ).all()

            if not published_rows and severity is None:
                seed = PublicReport(
                    id=str(uuid4()),
                    public_slug=f"threat-{uuid4().hex[:10]}",
                    title="Credential phishing kit indicators",
                    summary=(
                        "Sanitized community-facing report showing phishing "
                        "infrastructure indicators."
                    ),
                    severity=ThreatSeverity.MEDIUM.value,
                    indicator_count=3,
                    source_kind="workspace_publish",
                    status=PublicShareStatus.PUBLISHED.value,
                    created_at=datetime.now(timezone.utc),
                    approved_at=datetime.now(timezone.utc),
                )
                db.add(seed)
                db.commit()
                db.refresh(seed)
                published_rows = [seed]

        start_index = 0
        if cursor is not None:
            for index, report_row in enumerate(published_rows):
                if report_row.id == cursor:
                    start_index = index + 1
                    break

        paged_rows = published_rows[start_index : start_index + limit]
        next_cursor = None
        if start_index + limit < len(published_rows) and paged_rows:
            next_cursor = paged_rows[-1].id

        return PublicThreatListResponse(
            items=[_to_public_summary(row) for row in paged_rows],
            next_cursor=next_cursor,
        )

    def get_public_report(self, public_report_id: str) -> PublicThreatSummary | None:
        """Return a single public report if present."""
        _ensure_public_sharing_tables()
        with self._session_factory() as db:
            row = db.scalar(
                select(PublicReport).where(
                    PublicReport.id == public_report_id,
                    PublicReport.status == PublicShareStatus.PUBLISHED.value,
                )
            )
        if row is None:
            return None
        return _to_public_summary(row)
