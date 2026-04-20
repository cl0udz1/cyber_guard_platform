"""
Purpose:
    Additional source adapter placeholder to break the old single-source assumption.
Inputs:
    Extracted indicators and normalized artifact values.
Outputs:
    Deterministic scaffold enrichment summary.
Dependencies:
    None beyond the adapter shape.
TODO Checklist:
    - [ ] Rename this client once the team chooses a real source.
"""

from app.services.enrichment.base import (
    EnrichmentHitPayload,
    build_enrichment_hit_payload,
)


class SourceAClient:
    """Generic enrichment source placeholder A."""

    name = "source_a"

    async def enrich(
        self,
        indicators: list[str],
        artifact_value: str,
    ) -> EnrichmentHitPayload:
        """Return a deterministic placeholder summary for scaffold demos."""
        return build_enrichment_hit_payload(
            source_name=self.name,
            verdict="suspicious",
            confidence_score=72,
            summary=f"Source A correlated {len(indicators)} indicators with prior campaigns.",
        )
