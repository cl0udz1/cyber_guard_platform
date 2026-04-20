from pydantic import ValidationError

from app.schemas.artifact import ArtifactSubmissionRequest
from app.services.artifact_service import ArtifactService
from app.services.ioc_extraction_service import IocExtractionService
from app.services.normalization_service import NormalizationService
from app.utils.email_tools import extract_email_indicators, normalize_email_signal
from app.utils.enums import ArtifactType
from app.utils.hashing import detect_hash_algorithm, normalize_hash_value, sha256_text
from app.utils.url_tools import normalize_url


def test_artifact_submission_requires_file_name_for_file_inputs() -> None:
    try:
        ArtifactSubmissionRequest(
            workspace_id="demo-workspace",
            artifact_type=ArtifactType.FILE,
            artifact_value="raw file content",
        )
    except ValidationError as exc:
        assert "file_name is required" in str(exc)
    else:
        raise AssertionError("Expected file submissions without file_name to fail.")


def test_artifact_submission_trims_fields() -> None:
    payload = ArtifactSubmissionRequest(
        workspace_id=" demo-workspace ",
        artifact_type=ArtifactType.URL,
        artifact_value=" https://example.org/login ",
        notes="  analyst   note  ",
    )

    assert payload.workspace_id == "demo-workspace"
    assert payload.artifact_value == "https://example.org/login"
    assert payload.notes == "analyst note"


def test_normalization_service_handles_all_owned_artifact_lanes() -> None:
    service = NormalizationService()

    assert service.normalize(ArtifactType.URL, "Example.org/login") == "https://example.org/login"
    assert service.normalize(ArtifactType.EMAIL_SIGNAL, " Alert From ADMIN@Example.Org ") == "alert from admin@example.org"
    assert service.normalize(ArtifactType.HASH, "A" * 64) == "a" * 64
    assert service.normalize(ArtifactType.FILE, "sample file body") == sha256_text("sample file body")


def test_normalization_service_rejects_unsupported_hash_shape() -> None:
    service = NormalizationService()

    try:
        service.normalize(ArtifactType.HASH, "not-a-real-hash")
    except ValueError as exc:
        assert "MD5, SHA-1, or SHA-256" in str(exc)
    else:
        raise AssertionError("Expected invalid hash input to fail.")


def test_ioc_extraction_service_extracts_url_and_hostname() -> None:
    service = IocExtractionService()

    result = service.extract(ArtifactType.URL, "https://portal.example.org/login")

    assert result == ["https://portal.example.org/login", "portal.example.org"]


def test_ioc_extraction_service_extracts_email_signal_indicators() -> None:
    service = IocExtractionService()
    normalized = normalize_email_signal(
        "From ADMIN@Example.Org visit https://portal.example.org/login or portal.example.org"
    )

    result = service.extract(ArtifactType.EMAIL_SIGNAL, normalized)

    assert "admin@example.org" in result
    assert "https://portal.example.org/login" in result
    assert "portal.example.org" in result


def test_url_normalization_handles_missing_scheme_and_default_port() -> None:
    assert normalize_url("Example.org:443/login#fragment") == "https://example.org/login"


def test_email_signal_helpers_return_deduplicated_indicators() -> None:
    normalized = normalize_email_signal(
        "ADMIN@example.org admin@example.org https://example.org https://example.org"
    )

    assert normalized == "admin@example.org admin@example.org https://example.org https://example.org"
    assert extract_email_indicators(normalized) == ["admin@example.org", "https://example.org", "example.org"]


def test_hash_helpers_normalize_and_detect_algorithm() -> None:
    sha1_value = "A" * 40

    assert normalize_hash_value(sha1_value) == "a" * 40
    assert detect_hash_algorithm(sha1_value) == "sha1"


def test_artifact_service_returns_prepared_submission() -> None:
    payload = ArtifactSubmissionRequest(
        workspace_id="demo-workspace",
        artifact_type=ArtifactType.URL,
        artifact_value="https://example.org/login",
    )

    result = ArtifactService().prepare_submission(payload, "https://example.org/login")

    assert result.workspace_id == "demo-workspace"
    assert result.artifact_type == ArtifactType.URL
    assert result.normalized_value == "https://example.org/login"
    assert result.submission_id
