"""
Purpose:
    Scan job schemas describing orchestration state and source outputs.
Inputs:
    Scan submission routes and job polling endpoints.
Outputs:
    Typed async scan responses.
Dependencies:
    Pydantic models and scaffold enums.
TODO Checklist:
    - [ ] Add pagination/filter support for job history routes later.
    - [ ] Add richer worker/progress metadata only if the UI really needs it.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.artifact import ArtifactSubmissionRequest, ArtifactSubmissionResponse
from app.utils.enums import AiMode, ScanJobStatus


class SourceHit(BaseModel):
    """Compact per-source enrichment result."""

    source_name: str = Field(..., description="Name of the scaffold source that produced this hit.")
    verdict: str = Field(..., description="Simple verdict string returned by the source stub.")
    confidence_score: int = Field(..., description="Integer confidence score for lightweight UI display.")
    summary: str = Field(..., description="Short human-readable summary of the source response.")


class ScanJobCreateRequest(BaseModel):
    """Create scan job payload."""

    model_config = ConfigDict(extra="forbid")

    artifact: ArtifactSubmissionRequest = Field(..., description="Submitted artifact entering the scan pipeline.")
    ai_mode: AiMode = Field(default=AiMode.LOCAL, description="Requested AI mode for later orchestration steps.")


class ScanJobResponse(BaseModel):
    """Scan job status response."""

    scan_job_id: str = Field(..., description="Generated identifier for the scaffold scan job.")
    status: ScanJobStatus = Field(..., description="Current orchestration state for this job.")
    artifact: ArtifactSubmissionResponse = Field(..., description="Accepted artifact after intake normalization.")
    ai_mode: AiMode = Field(..., description="AI mode attached to the job request.")
    sources: list[SourceHit] = Field(..., description="Collected per-source hits accumulated by orchestration.")
    report_id: str | None = Field(default=None, description="Optional future report identifier.")
    created_at: datetime = Field(..., description="UTC timestamp for job creation.")
    completed_at: datetime | None = Field(default=None, description="UTC timestamp for job completion, if any.")
