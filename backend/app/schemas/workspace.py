"""
Purpose:
    Workspace request and response schemas.
Inputs:
    Workspace creation, selection, and listing routes.
Outputs:
    Typed workspace payloads for backend/frontend coordination.
Dependencies:
    Pydantic models.
TODO Checklist:
    - [ ] Add retention and sharing-policy settings once those controls are implemented.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WorkspaceCreateRequest(BaseModel):
    """Create workspace payload."""

    model_config = ConfigDict(extra="forbid")

    organization_id: str
    name: str = Field(..., min_length=2, max_length=160)
    slug: str = Field(..., min_length=2, max_length=160)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Collapse whitespace in workspace names."""
        return " ".join(part for part in value.strip().split() if part)

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        """Normalize slugs into lowercase hyphenated identifiers."""
        normalized = "-".join(part for part in value.strip().lower().replace("_", "-").split() if part)
        if not normalized:
            raise ValueError("Slug must not be empty.")
        return normalized


class WorkspaceResponse(BaseModel):
    """Workspace summary response."""

    model_config = ConfigDict(extra="forbid")

    id: str
    organization_id: str
    name: str
    slug: str
    created_at: datetime
    membership_count: int = 0

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Keep workspace names neatly trimmed in responses."""
        return " ".join(part for part in value.strip().split() if part)

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        """Keep workspace slugs normalized in responses."""
        normalized = "-".join(part for part in value.strip().lower().replace("_", "-").split() if part)
        if not normalized:
            raise ValueError("Slug must not be empty.")
        return normalized
