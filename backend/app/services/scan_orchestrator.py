"""
Purpose:
    Coordinate artifact normalization, IOC extraction, enrichment, optional AI, and report creation.
Owner:
    Primary: 220042711 - OMAR ABDURASHEED
    Coordinate with: 220053973 - FARIS BIN SUMAYDI for pipeline entry assumptions
Inputs:
    Scan job creation requests from API routes.
Outputs:
    Scan job responses and stored report artifacts for later retrieval.
Dependencies:
    Artifact, normalization, extraction, cache, enrichment, AI, and report services.
TODO Checklist:
    - [ ] Move long-running execution to a real background worker.
    - [ ] Persist job state to the database instead of process memory.
    - [ ] Add retry/error handling per adapter when integrations are implemented.
    - [ ] Keep this file orchestration-focused; do not bury route or UI logic here.
"""

from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.scan import ScanJobCreateRequest, ScanJobResponse, SourceHit
from app.services.artifact_service import ArtifactService
from app.services.caching_service import CachingService
from app.services.ioc_extraction_service import IocExtractionService
from app.services.normalization_service import NormalizationService
from app.services.report_service import ReportService


class ScanOrchestrator:
    """Scaffold orchestrator for async-style scan jobs."""

    def __init__(
        self,
        artifact_service: ArtifactService,
        normalization_service: NormalizationService,
        ioc_extraction_service: IocExtractionService,
        caching_service: CachingService,
        enrichment_adapters: list[object],
        ai_services: dict[str, object],
        report_service: ReportService,
    ) -> None:
        self.artifact_service = artifact_service
        self.normalization_service = normalization_service
        self.ioc_extraction_service = ioc_extraction_service
        self.caching_service = caching_service
        self.enrichment_adapters = enrichment_adapters
        self.ai_services = ai_services
        self.report_service = report_service
        self._jobs: dict[str, ScanJobResponse] = {}

    async def start_scan(self, payload: ScanJobCreateRequest) -> ScanJobResponse:
        """Execute the scaffold pipeline synchronously while exposing async job semantics."""
        normalized_value = self.normalization_service.normalize(
            payload.artifact.artifact_type,
            payload.artifact.artifact_value,
        )
        cache_key = f"{payload.artifact.artifact_type.value}:{normalized_value}:{payload.ai_mode.value}"
        cached = self.caching_service.get_scan(cache_key)
        if cached is not None:
            return cached

        artifact = self.artifact_service.prepare_submission(payload.artifact, normalized_value)
        indicators = self.ioc_extraction_service.extract(payload.artifact.artifact_type, normalized_value)

        source_hits: list[SourceHit] = []
        for adapter in self.enrichment_adapters:
            result = await adapter.enrich(indicators=indicators, artifact_value=normalized_value)
            source_hits.append(SourceHit(**result))

        ai_summary = None
        if payload.ai_mode.value in self.ai_services:
            ai_summary = await self.ai_services[payload.ai_mode.value].analyze(
                artifact_value=normalized_value,
                indicators=indicators,
                source_hits=source_hits,
            )

        scan_job_id = str(uuid4())
        report = await self.report_service.build_report(
            scan_job_id=scan_job_id,
            artifact=artifact,
            source_hits=source_hits,
            ai_summary=ai_summary,
        )

        response = ScanJobResponse(
            scan_job_id=scan_job_id,
            status="completed",
            artifact=artifact,
            ai_mode=payload.ai_mode,
            sources=source_hits,
            report_id=report.report_id,
            created_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        self._jobs[scan_job_id] = response
        self.caching_service.set_scan(cache_key, response)
        return response

    def get_job(self, scan_job_id: str) -> ScanJobResponse | None:
        """Return a single job response if the scaffold already built it."""
        return self._jobs.get(scan_job_id)

    def list_jobs(self) -> list[ScanJobResponse]:
        """Return all known job responses in memory."""
        return list(self._jobs.values())
