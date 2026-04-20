"""
Purpose:
    User and membership schemas for workspace-aware account views.
Inputs:
    User profile and membership data from auth and user routes.
Outputs:
    Typed responses for frontend account/workspace context.
Dependencies:
    Pydantic models.
TODO Checklist:
    - [ ] Add invitation status once org onboarding is implemented.
    - [ ] Add profile editing request schemas if needed later.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.permissions import PLATFORM_ROLES, normalize_role


class MembershipSummary(BaseModel):
    """Compact membership view for account and workspace pages."""

    model_config = ConfigDict(extra="forbid")

    organization_id: str
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


class UserProfileResponse(BaseModel):
    """Current user profile response."""

    model_config = ConfigDict(extra="forbid")

    id: str
    display_name: str
    email: str
    platform_role: str
    memberships: list[MembershipSummary]
    created_at: datetime

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        """Keep profile emails normalized in API responses."""
        return value.strip().lower()

    @field_validator("platform_role")
    @classmethod
    def normalize_known_role(cls, value: str) -> str:
        """Keep profile roles aligned with shared RBAC helpers."""
        normalized = normalize_role(value)
        if normalized not in PLATFORM_ROLES:
            raise ValueError(f"Unsupported role '{value}'.")
        return normalized


class UserSummaryResponse(BaseModel):
    """Compact user view used in organization membership lists."""

    model_config = ConfigDict(extra="forbid")

    id: str
    display_name: str
    email: str
    platform_role: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        """Keep user emails normalized in API responses."""
        return value.strip().lower()

    @field_validator("platform_role")
    @classmethod
    def normalize_known_role(cls, value: str) -> str:
        """Keep compact user views aligned with RBAC helpers."""
        normalized = normalize_role(value)
        if normalized not in PLATFORM_ROLES:
            raise ValueError(f"Unsupported role '{value}'.")
        return normalized


class MembershipAssignmentRequest(BaseModel):
    """Request payload for assigning a user into an organization or workspace."""

    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(..., min_length=1)
    organization_id: str = Field(..., min_length=1)
    workspace_id: str | None = None
    role: str = Field(default="analyst")

    @field_validator("role")
    @classmethod
    def normalize_known_role(cls, value: str) -> str:
        """Keep assigned roles aligned with shared RBAC helpers."""
        normalized = normalize_role(value)
        if normalized not in PLATFORM_ROLES:
            raise ValueError(f"Unsupported role '{value}'.")
        return normalized
