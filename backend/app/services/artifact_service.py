"""
Purpose:
    Prepare artifact submissions before scan orchestration begins.
Inputs:
    Artifact submission requests and normalized values.
Outputs:
    Typed artifact submission responses that routes can echo back immediately.
Dependencies:
    Artifact schemas and hashing helpers.
TODO Checklist:
    - [ ] Add object-storage references for real file uploads.
    - [ ] Add artifact retention metadata when deletion rules are agreed.
"""

from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.artifact import ArtifactSubmissionRequest, ArtifactSubmissionResponse


class ArtifactService:
    """Lightweight artifact preparation service."""

    def prepare_submission(
        self,
        payload: ArtifactSubmissionRequest,
        normalized_value: str,
    ) -> ArtifactSubmissionResponse:
        """Return the accepted artifact record passed into the scan job response."""
        return ArtifactSubmissionResponse(
            submission_id=str(uuid4()),
            workspace_id=payload.workspace_id,
            artifact_type=payload.artifact_type,
            normalized_value=normalized_value,
            created_at=datetime.now(timezone.utc),
        )
