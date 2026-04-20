"""
Purpose:
    Enforce the public/private data separation rule for shared threat content.
Inputs:
    Private report metadata and proposed public payloads.
Outputs:
    Sanitized public-safe payloads with obvious identity fields removed.
Dependencies:
    Standard library string helpers.
TODO Checklist:
    - [ ] Add stronger content scanning for names, emails, and internal IDs.
    - [ ] Add unit tests for organization/workspace leakage scenarios.
"""

import re

from fastapi import HTTPException, status


FORBIDDEN_PUBLIC_KEYS = {
    "organization_id",
    "workspace_id",
    "user_id",
    "email",
    "owner_name",
    "private_report_id",
}

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
UUID_PATTERN = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b")
WORKSPACE_ORG_ID_PATTERN = re.compile(r"\b(workspace|organization|user)[-_ ]?id\b", re.IGNORECASE)
UNSAFE_QUERY_PATTERN = re.compile(r"\?.*?(workspace|organization|user)[^=&\s]*=", re.IGNORECASE)
URL_QUERY_PATTERN = re.compile(r"(https?://[^\s?#]+)\?[^\s#]+")


def _flatten_payload_values(payload: object) -> list[str]:
    """Flatten nested payload values into strings for pattern scanning."""
    values: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            values.append(str(key))
            values.extend(_flatten_payload_values(value))
    elif isinstance(payload, list):
        for item in payload:
            values.extend(_flatten_payload_values(item))
    elif payload is not None:
        values.append(str(payload))
    return values


class SanitizationService:
    """Guardrail service for Disconnect by Design publication rules."""

    def assert_identity_safe(self, payload: dict[str, object]) -> None:
        """Reject payloads that include direct identity or workspace link fields."""
        forbidden = FORBIDDEN_PUBLIC_KEYS.intersection(payload.keys())
        if forbidden:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Public payload contains forbidden identity fields: {sorted(forbidden)}",
            )

        values = _flatten_payload_values(payload)
        if any(EMAIL_PATTERN.search(value) for value in values):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Public payload appears to contain an email address.",
            )
        if any(UUID_PATTERN.search(value) for value in values):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Public payload appears to contain an internal identifier.",
            )
        if any(WORKSPACE_ORG_ID_PATTERN.search(value) for value in values):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Public payload appears to reference private identity fields.",
            )
        if any(UNSAFE_QUERY_PATTERN.search(value) for value in values):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Public payload includes query parameters that can expose private scope.",
            )

    def sanitize_summary(self, summary: str) -> str:
        """Apply a lightweight text sanitization pass for scaffold demos."""
        sanitized = summary.replace("workspace", "private scope").replace("organization", "publisher")
        sanitized = EMAIL_PATTERN.sub("[redacted-email]", sanitized)
        sanitized = UUID_PATTERN.sub("[redacted-id]", sanitized)
        sanitized = URL_QUERY_PATTERN.sub(r"\1", sanitized)
        return sanitized
