"""
Purpose:
    Maintain the scaffold moderation queue for publish requests and external uploads.
Inputs:
    Review creation requests and reviewer decisions.
Outputs:
    Queue items and decision echoes used by admin routes.
Dependencies:
    Admin review schemas.
TODO Checklist:
    - [ ] Replace in-memory queue with DB persistence.
    - [ ] Add audit history and reviewer identity tracking.
"""

from datetime import datetime, timezone
from collections.abc import Callable
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.admin_review import AdminReview
from app.schemas.admin_review import (
    AdminReviewDecisionRequest,
    AdminReviewDecisionResponse,
    AdminReviewQueueItem,
)


_tables_ready = False


def _ensure_admin_review_tables() -> None:
    """Create admin-review related tables on first use for scaffold persistence."""
    global _tables_ready
    if _tables_ready:
        return
    Base.metadata.create_all(bind=engine)
    _tables_ready = True


def _to_queue_item(model: AdminReview) -> AdminReviewQueueItem:
    """Convert ORM moderation row to API queue item."""
    return AdminReviewQueueItem(
        review_id=model.id,
        review_type=model.review_type,
        status=model.status,
        requested_action=model.requested_action,
        summary=model.summary,
        created_at=model.created_at,
    )


class AdminReviewService:
    """Moderation queue service backed by scaffold database tables."""

    def __init__(self, session_factory: Callable[[], Session] = SessionLocal) -> None:
        self._session_factory = session_factory

    def create_review(
        self,
        review_type: str,
        summary: str,
        submission_reference: str | None = None,
        requested_action: str = "publish",
    ) -> AdminReviewQueueItem:
        """Add a scaffold queue item and return it."""
        _ensure_admin_review_tables()
        review_row = AdminReview(
            id=str(uuid4()),
            review_type=review_type,
            submission_reference=submission_reference or str(uuid4()),
            summary=summary,
            status="pending",
            requested_action=requested_action,
            created_at=datetime.now(timezone.utc),
        )
        with self._session_factory() as db:
            db.add(review_row)
            db.commit()
            db.refresh(review_row)
        return _to_queue_item(review_row)

    def list_queue(self) -> list[AdminReviewQueueItem]:
        """Return review items in insertion order."""
        _ensure_admin_review_tables()
        with self._session_factory() as db:
            rows = db.scalars(
                select(AdminReview)
                .where(AdminReview.status.in_(["pending", "needs_changes"]))
                .order_by(AdminReview.created_at.desc())
            ).all()
        return [_to_queue_item(row) for row in rows]

    def decide(
        self,
        review_id: str,
        payload: AdminReviewDecisionRequest,
    ) -> AdminReviewDecisionResponse:
        """Apply a decision to a review queue item."""
        _ensure_admin_review_tables()
        resolved_status = "pending"
        with self._session_factory() as db:
            review_row = db.get(AdminReview, review_id)
            if review_row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Review item not found.",
                )

            if review_row.status in {"approved", "rejected"}:
                if review_row.decision == payload.decision:
                    return AdminReviewDecisionResponse(
                        review_id=review_id,
                        decision=payload.decision,
                        status=review_row.status,
                    )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Review item is already finalized.",
                )

            if payload.decision == "approve":
                review_row.status = "approved"
            elif payload.decision == "reject":
                review_row.status = "rejected"
            else:
                review_row.status = "needs_changes"

            review_row.decision = payload.decision
            review_row.reviewer_notes = payload.reviewer_notes
            review_row.decided_at = datetime.now(timezone.utc)
            resolved_status = review_row.status
            db.add(review_row)
            db.commit()

        return AdminReviewDecisionResponse(
            review_id=review_id,
            decision=payload.decision,
            status=resolved_status,
        )

    def get_submission_context(self, review_id: str) -> tuple[str, str] | None:
        """Return review type and submission reference for downstream publishing hooks."""
        _ensure_admin_review_tables()
        with self._session_factory() as db:
            review_row = db.get(AdminReview, review_id)
            if review_row is None:
                return None
            return review_row.review_type, review_row.submission_reference
