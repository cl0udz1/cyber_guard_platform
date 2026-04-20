import asyncio

from app.schemas.artifact import ArtifactSubmissionRequest
from app.schemas.scan import ScanJobCreateRequest
from app.services.ai.local_ai_service import LocalAiService
from app.services.artifact_service import ArtifactService
from app.services.caching_service import CachingService
from app.services.enrichment.source_a_client import SourceAClient
from app.services.enrichment.virustotal_client import VirusTotalClient
from app.services.ioc_extraction_service import IocExtractionService
from app.services.normalization_service import NormalizationService
from app.services.report_service import ReportService
from app.services.scan_orchestrator import ScanOrchestrator
from app.utils.enums import AiMode, ArtifactType


class BrokenAdapter:
    """Test-only adapter that simulates one source failing mid-scan."""

    name = "broken_adapter"

    async def enrich(self, indicators: list[str], artifact_value: str) -> dict[str, object]:
        raise RuntimeError("adapter unavailable")


def test_scan_orchestrator_caches_completed_scans_and_builds_report() -> None:
    async def run():
        report_service = ReportService()
        orchestrator = ScanOrchestrator(
            artifact_service=ArtifactService(),
            normalization_service=NormalizationService(),
            ioc_extraction_service=IocExtractionService(),
            caching_service=CachingService(),
            enrichment_adapters=[
                VirusTotalClient(api_key="", base_url="https://example.test", timeout_seconds=5),
                SourceAClient(),
            ],
            ai_services={"local": LocalAiService(enabled=True)},
            report_service=report_service,
        )
        payload = ScanJobCreateRequest(
            artifact=ArtifactSubmissionRequest(
                workspace_id="demo-workspace",
                artifact_type=ArtifactType.URL,
                artifact_value="http://10.0.0.4/login?redirect=account&token=abc123",
            ),
            ai_mode=AiMode.LOCAL,
        )

        first = await orchestrator.start_scan(payload)
        second = await orchestrator.start_scan(payload)
        return report_service, orchestrator, first, second

    report_service, orchestrator, first, second = asyncio.run(run())
    report = report_service.get_report(first.report_id)

    assert first.scan_job_id == second.scan_job_id
    assert report is not None
    assert report.ai_summary is not None
    assert report.ai_summary.startswith("Local AI mode reviewed")
    assert orchestrator.list_jobs()[0].scan_job_id == first.scan_job_id


def test_scan_orchestrator_keeps_other_sources_when_one_adapter_fails() -> None:
    async def run():
        orchestrator = ScanOrchestrator(
            artifact_service=ArtifactService(),
            normalization_service=NormalizationService(),
            ioc_extraction_service=IocExtractionService(),
            caching_service=CachingService(),
            enrichment_adapters=[
                BrokenAdapter(),
                SourceAClient(),
            ],
            ai_services={"local": LocalAiService(enabled=True)},
            report_service=ReportService(),
        )
        payload = ScanJobCreateRequest(
            artifact=ArtifactSubmissionRequest(
                workspace_id="demo-workspace",
                artifact_type=ArtifactType.URL,
                artifact_value="https://example.org/login",
            ),
            ai_mode=AiMode.LOCAL,
        )
        return await orchestrator.start_scan(payload)

    result = asyncio.run(run())

    assert {hit.source_name for hit in result.sources} == {"broken_adapter", "source_a"}
    assert any("unavailable during this scan" in hit.summary for hit in result.sources)
