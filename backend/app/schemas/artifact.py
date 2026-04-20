"""
Purpose:
    Artifact submission schemas covering file/hash/URL/email-signal inputs.
Inputs:
    Scan submission requests from authenticated users or organizations.
Outputs:
    Typed artifact payloads used by scan job routes and services.
Dependencies:
    Pydantic models and scaffold enums.
TODO Checklist:
    - [ ] Split file upload metadata from pasted values if multipart support is added.
    - [ ] Add stronger validation per artifact type once validators are implemented.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.utils.enums import ArtifactType


class ArtifactSubmissionRequest(BaseModel):
    """Create a private artifact submission."""

    model_config = ConfigDict(extra="forbid")

    workspace_id: str = Field(..., description="Workspace that owns the private submission.")
    artifact_type: ArtifactType = Field(..., description="High-level intake lane for the submitted value.")
    artifact_value: str = Field(
        ...,
        min_length=2,
        max_length=10000,
        description="Raw user-provided value before normalization.",
    )
    file_name: str | None = Field(
        default=None,
        max_length=255,
        description="Optional original filename for future file-upload support.",
    )
    notes: str | None = Field(
        default=None,
        max_length=500,
        description="Optional analyst note stored with the submission scaffold.",
    )

    @model_validator(mode="after")
    def validate_submission_shape(self) -> "ArtifactSubmissionRequest":
        """Apply simple cross-field validation that keeps intake paths obvious."""
        self.workspace_id = self.workspace_id.strip()
        self.artifact_value = self.artifact_value.strip()

        if not self.workspace_id:
            raise ValueError("workspace_id cannot be blank.")
        if not self.artifact_value:
            raise ValueError("artifact_value cannot be blank.")

        if self.file_name is not None:
            self.file_name = self.file_name.strip() or None
        if self.notes is not None:
            self.notes = " ".join(self.notes.split()) or None

        if self.artifact_type == ArtifactType.FILE and not self.file_name:
            raise ValueError("file_name is required when artifact_type is file.")

        return self


class ArtifactSubmissionResponse(BaseModel):
    """Echo of the accepted artifact submission."""

    submission_id: str = Field(..., description="Generated identifier for the accepted submission.")
    workspace_id: str = Field(..., description="Workspace that owns the submission.")
    artifact_type: ArtifactType = Field(..., description="Artifact lane used by normalization and scan intake.")
    normalized_value: str = Field(..., description="Canonical artifact form passed into the scaffold pipeline.")
    created_at: datetime = Field(..., description="UTC timestamp recorded when the submission was prepared.")
