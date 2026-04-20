"""
Purpose:
    Optional extra source adapter placeholder left disabled by default.
Inputs:
    Extracted indicators and normalized artifact values.
Outputs:
    Deterministic scaffold enrichment summary.
Dependencies:
    None beyond the adapter shape.
TODO Checklist:
    - [ ] Use this slot for a student-selected enrichment source if time allows.
"""

from app.services.enrichment.base import (
    EnrichmentHitPayload,
    build_enrichment_hit_payload,
)


class SourceCClient:
    """Generic enrichment source placeholder C."""

    name = "source_c"

    async def enrich(
        self,
        indicators: list[str],
        artifact_value: str,
    ) -> EnrichmentHitPayload:
        """Return a deterministic placeholder summary for scaffold demos."""
        return build_enrichment_hit_payload(
            source_name=self.name,
            verdict="informational",
            confidence_score=40,
            summary=f"Source C contributed contextual telemetry for {len(indicators)} indicators.",
        )
