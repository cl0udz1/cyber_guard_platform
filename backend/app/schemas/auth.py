"""
Purpose:
    Authentication and principal schemas for the refreshed scaffold.
Inputs:
    Auth route payloads and dependency-resolved principal state.
Outputs:
    Typed request/response models used across backend and tests.
Dependencies:
    Pydantic models and validation helpers.
TODO Checklist:
    - [ ] Add invitation acceptance and password reset schemas later.
    - [ ] Replace demo fields with real registration data once auth is implemented.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.permissions import PLATFORM_ROLES, normalize_role


AccountType = Literal["user", "organization"]


class RegisterRequest(BaseModel):
    """Scaffold registration payload for individual or organization-linked users."""

    model_config = ConfigDict(extra="forbid")

    display_name: str = Field(..., min_length=2, max_length=120)
    email: str
    password: str = Field(..., min_length=8, max_length=128)
    account_type: AccountType = "user"

    @field_validator("display_name")
    @classmethod
    def normalize_display_name(cls, value: str) -> str:
        """Keep scaffold display names trimmed and readable."""
        normalized = " ".join(part for part in value.strip().split() if part)
        if len(normalized) < 2:
            raise ValueError("Display name must contain at least 2 characters.")
        return normalized

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        """Trim and lowercase emails for deterministic login behavior."""
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("Email must look like a valid address.")
        return normalized


class LoginRequest(BaseModel):
    """Scaffold login payload."""

    model_config = ConfigDict(extra="forbid")

    email: str
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        """Trim and lowercase emails for deterministic demo login behavior."""
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("Email must look like a valid address.")
        return normalized


class TokenResponse(BaseModel):
    """Bearer token response used by the scaffold frontend."""

    model_config = ConfigDict(extra="forbid")

    access_token: str
    token_type: str = "bearer"
    principal_role: str
    organization_id: str | None = None
    workspace_id: str | None = None

    @field_validator("principal_role")
    @classmethod
    def normalize_known_role(cls, value: str) -> str:
        """Keep token responses aligned with shared RBAC helpers."""
        normalized = normalize_role(value)
        if normalized not in PLATFORM_ROLES:
            raise ValueError(f"Unsupported role '{value}'.")
        return normalized


class CurrentPrincipal(BaseModel):
    """Lightweight current-user context resolved from JWT claims."""

    model_config = ConfigDict(extra="ignore")

    subject: str
    email: str
    role: str
    organization_id: str | None = None
    workspace_id: str | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        """Keep principal emails normalized for lookups."""
        return value.strip().lower()

    @field_validator("role")
    @classmethod
    def normalize_known_role(cls, value: str) -> str:
        """Normalize role casing and reject unknown scaffold roles."""
        normalized = normalize_role(value)
        if normalized not in PLATFORM_ROLES:
            raise ValueError(f"Unsupported role '{value}'.")
        return normalized
