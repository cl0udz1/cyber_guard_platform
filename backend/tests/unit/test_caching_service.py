from datetime import datetime, timedelta, timezone

from app.schemas.artifact import ArtifactSubmissionResponse
from app.schemas.scan import ScanJobResponse
from app.services.caching_service import CachingService
from app.utils.enums import AiMode, ArtifactType, ScanJobStatus


def _build_response(scan_job_id: str = "scan-1") -> ScanJobResponse:
    created_at = datetime(2026, 3, 26, 12, 0, tzinfo=timezone.utc)
    return ScanJobResponse(
        scan_job_id=scan_job_id,
        status=ScanJobStatus.COMPLETED,
        artifact=ArtifactSubmissionResponse(
            submission_id="submission-1",
            workspace_id="demo-workspace",
            artifact_type=ArtifactType.URL,
            normalized_value="https://example.org/login",
            created_at=created_at,
        ),
        ai_mode=AiMode.LOCAL,
        sources=[],
        report_id="report-1",
        created_at=created_at,
        completed_at=created_at,
    )


def test_build_scan_key_is_stable_and_compact() -> None:
    service = CachingService()

    key_one = service.build_scan_key("url", "https://example.org/login", "local")
    key_two = service.build_scan_key("url", "https://example.org/login", "local")

    assert key_one == key_two
    assert key_one.startswith("scan:")
    assert len(key_one) < 80


def test_cache_expires_entries_using_ttl() -> None:
    state = {"now": datetime(2026, 3, 26, 12, 0, tzinfo=timezone.utc)}
    service = CachingService(ttl_seconds=30, time_provider=lambda: state["now"])
    key = service.build_scan_key("url", "https://example.org/login", "local")

    service.set_scan(key, _build_response())
    assert service.get_scan(key) is not None
    assert service.cache_size() == 1

    state["now"] = state["now"] + timedelta(seconds=31)

    assert service.get_scan(key) is None
    assert service.cache_size() == 0
