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
from typing import Protocol
from uuid import uuid4

from app.schemas.scan import ScanJobCreateRequest, ScanJobResponse, SourceHit
from app.services.artifact_service import ArtifactService
from app.services.caching_service import CachingService
from app.services.enrichment.base import EnrichmentAdapter, build_enrichment_hit_payload
from app.services.ioc_extraction_service import IocExtractionService
from app.services.normalization_service import NormalizationService
from app.services.report_service import ReportService
from app.utils.enums import ScanJobStatus


class AiAnalysisService(Protocol):
    """Shared analyze interface for scaffold AI services."""

    async def analyze(
        self,
        artifact_value: str,
        indicators: list[str],
        source_hits: list[SourceHit],
    ) -> str | None:
        """Return an optional AI summary payload for a completed scan."""


class ScanOrchestrator:
    """Scaffold orchestrator for async-style scan jobs."""

    def __init__(
        self,
        artifact_service: ArtifactService,
        normalization_service: NormalizationService,
        ioc_extraction_service: IocExtractionService,
        caching_service: CachingService,
        enrichment_adapters: list[EnrichmentAdapter],
        ai_services: dict[str, AiAnalysisService],
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
        cache_key = self.caching_service.build_scan_key(
            artifact_type=payload.artifact.artifact_type.value,
            artifact_value=normalized_value,
            ai_mode=payload.ai_mode.value,
        )
        cached = self.caching_service.get_scan(cache_key)
        if cached is not None:
            return cached

        scan_job_id = str(uuid4())
        created_at = datetime.now(timezone.utc)
        artifact = self.artifact_service.prepare_submission(payload.artifact, normalized_value)
        self._jobs[scan_job_id] = self._build_job_response(
            scan_job_id=scan_job_id,
            artifact=artifact,
            ai_mode=payload.ai_mode,
            status=ScanJobStatus.NORMALIZING,
            sources=[],
            report_id=None,
            created_at=created_at,
            completed_at=None,
        )
        source_hits: list[SourceHit] = []

        try:
            indicators = self.ioc_extraction_service.extract(
                payload.artifact.artifact_type,
                normalized_value,
            )
            self._jobs[scan_job_id] = self._build_job_response(
                scan_job_id=scan_job_id,
                artifact=artifact,
                ai_mode=payload.ai_mode,
                status=ScanJobStatus.ENRICHING,
                sources=[],
                report_id=None,
                created_at=created_at,
                completed_at=None,
            )
            source_hits = await self._collect_source_hits(
                indicators=indicators,
                artifact_value=normalized_value,
            )
            self._jobs[scan_job_id] = self._build_job_response(
                scan_job_id=scan_job_id,
                artifact=artifact,
                ai_mode=payload.ai_mode,
                status=ScanJobStatus.REPORTING,
                sources=source_hits,
                report_id=None,
                created_at=created_at,
                completed_at=None,
            )
            ai_summary = await self._build_ai_summary(
                ai_mode=payload.ai_mode.value,
                artifact_value=normalized_value,
                indicators=indicators,
                source_hits=source_hits,
            )
            report = await self.report_service.build_report(
                scan_job_id=scan_job_id,
                artifact=artifact,
                source_hits=source_hits,
                ai_summary=ai_summary,
            )
        except Exception:
            self._jobs[scan_job_id] = self._build_job_response(
                scan_job_id=scan_job_id,
                artifact=artifact,
                ai_mode=payload.ai_mode,
                status=ScanJobStatus.FAILED,
                sources=source_hits,
                report_id=None,
                created_at=created_at,
                completed_at=datetime.now(timezone.utc),
            )
            raise

        response = self._build_job_response(
            scan_job_id=scan_job_id,
            artifact=artifact,
            ai_mode=payload.ai_mode,
            status=ScanJobStatus.COMPLETED,
            sources=source_hits,
            report_id=report.report_id,
            created_at=created_at,
            completed_at=datetime.now(timezone.utc),
        )
        self._jobs[scan_job_id] = response
        self.caching_service.set_scan(cache_key, response)
        return response

    async def _collect_source_hits(
        self,
        indicators: list[str],
        artifact_value: str,
    ) -> list[SourceHit]:
        """Collect source hits from each configured enrichment adapter."""
        source_hits: list[SourceHit] = []
        for adapter in self.enrichment_adapters:
            try:
                result = await adapter.enrich(indicators=indicators, artifact_value=artifact_value)
            except Exception as exc:
                source_name = getattr(adapter, "name", adapter.__class__.__name__.lower())
                result = build_enrichment_hit_payload(
                    source_name=source_name,
                    verdict="informational",
                    confidence_score=0,
                    summary=(
                        f"{source_name} was unavailable during this scan "
                        f"({exc.__class__.__name__})."
                    ),
                )
            source_hits.append(SourceHit(**result))
        return source_hits

    async def _build_ai_summary(
        self,
        ai_mode: str,
        artifact_value: str,
        indicators: list[str],
        source_hits: list[SourceHit],
    ) -> str | None:
        """Run the selected AI service when the current mode is enabled."""
        ai_service = self.ai_services.get(ai_mode)
        if ai_service is None:
            return None

        return await ai_service.analyze(
            artifact_value=artifact_value,
            indicators=indicators,
            source_hits=source_hits,
        )

    def get_job(self, scan_job_id: str) -> ScanJobResponse | None:
        """Return a single job response if the scaffold already built it."""
        return self._jobs.get(scan_job_id)

    def list_jobs(self) -> list[ScanJobResponse]:
        """Return all known job responses in memory."""
        return sorted(
            self._jobs.values(),
            key=lambda job: job.created_at,
            reverse=True,
        )

    def _build_job_response(
        self,
        scan_job_id: str,
        artifact,
        ai_mode,
        status: ScanJobStatus,
        sources: list[SourceHit],
        report_id: str | None,
        created_at: datetime,
        completed_at: datetime | None,
    ) -> ScanJobResponse:
        """Build one scan job response snapshot for the current orchestration stage."""
        return ScanJobResponse(
            scan_job_id=scan_job_id,
            status=status,
            artifact=artifact,
            ai_mode=ai_mode,
            sources=sources,
            report_id=report_id,
            created_at=created_at,
            completed_at=completed_at,
        )
