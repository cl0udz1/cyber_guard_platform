from fastapi import HTTPException

from app.services.sanitization_service import SanitizationService


def test_sanitizer_rejects_identity_fields() -> None:
    service = SanitizationService()

    try:
        service.assert_identity_safe({"title": "safe", "organization_id": "demo-org"})
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("Expected identity-safe validation to fail.")


def test_sanitizer_rewrites_sensitive_summary_terms() -> None:
    service = SanitizationService()
    result = service.sanitize_summary("Share workspace findings with the organization.")

    assert "workspace" not in result
    assert "organization" not in result


def test_sanitizer_rejects_email_values() -> None:
    service = SanitizationService()

    try:
        service.assert_identity_safe({"summary": "Send updates to analyst@example.edu"})
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("Expected identity-safe validation to reject email payload.")


def test_sanitizer_rejects_uuid_like_identifiers() -> None:
    service = SanitizationService()

    try:
        service.assert_identity_safe({"summary": "Linked internal id 123e4567-e89b-12d3-a456-426614174000"})
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("Expected identity-safe validation to reject UUID payload.")


def test_sanitizer_rejects_unsafe_query_params() -> None:
    service = SanitizationService()

    try:
        service.assert_identity_safe(
            {"reference": "https://example.org/threat?workspace_id=demo-workspace"}
        )
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("Expected identity-safe validation to reject unsafe query payload.")


def test_sanitizer_scrubs_email_and_query_in_summary() -> None:
    service = SanitizationService()

    result = service.sanitize_summary(
        "Contact admin@example.org and inspect https://example.org/path?workspace_id=demo-workspace"
    )

    assert "@" not in result
    assert "?workspace_id=" not in result
