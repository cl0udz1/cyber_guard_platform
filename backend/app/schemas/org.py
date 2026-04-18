"""
Purpose:
    Organization and membership contract shapes for scaffold planning.
Inputs:
    Organization creation/update flows and membership listings.
Outputs:
    Typed org route payloads.
Dependencies:
    Pydantic models.
TODO Checklist:
    - [ ] Add invitation requests and acceptance flow in a later phase.
    - [ ] Add organization settings schemas if governance rules become configurable.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.permissions import PLATFORM_ROLES, normalize_role


class OrganizationCreateRequest(BaseModel):
    """Create organization payload."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=2, max_length=160)
    slug: str = Field(..., min_length=2, max_length=160)
    sector: str | None = Field(default=None, max_length=80)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Collapse whitespace in org names."""
        return " ".join(part for part in value.strip().split() if part)

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        """Normalize slugs into lowercase hyphenated identifiers."""
        normalized = "-".join(part for part in value.strip().lower().replace("_", "-").split() if part)
        if not normalized:
            raise ValueError("Slug must not be empty.")
        return normalized


class OrganizationResponse(BaseModel):
    """Organization summary response."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    slug: str
    sector: str | None = None
    created_at: datetime
    membership_count: int = 0

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Keep organization names neatly trimmed in responses."""
        return " ".join(part for part in value.strip().split() if part)

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        """Keep organization slugs normalized in responses."""
        normalized = "-".join(part for part in value.strip().lower().replace("_", "-").split() if part)
        if not normalized:
            raise ValueError("Slug must not be empty.")
        return normalized


class MembershipResponse(BaseModel):
    """Membership summary for organization views."""

    model_config = ConfigDict(extra="forbid")

    user_id: str
    workspace_id: str | None = None
    role: str

    @field_validator("role")
    @classmethod
    def normalize_known_role(cls, value: str) -> str:
        """Keep membership roles aligned with shared RBAC helpers."""
        normalized = normalize_role(value)
        if normalized not in PLATFORM_ROLES:
            raise ValueError(f"Unsupported role '{value}'.")
        return normalized
