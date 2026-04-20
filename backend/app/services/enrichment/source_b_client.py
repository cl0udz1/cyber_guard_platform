"""
Purpose:
    Additional source adapter placeholder for reputation or sandbox-style enrichment.
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


class SourceBClient:
    """Generic enrichment source placeholder B."""

    name = "source_b"

    async def enrich(
        self,
        indicators: list[str],
        artifact_value: str,
    ) -> EnrichmentHitPayload:
        """Return a deterministic placeholder summary for scaffold demos."""
        return build_enrichment_hit_payload(
            source_name=self.name,
            verdict="malicious",
            confidence_score=84,
            summary=f"Source B flagged high-risk overlap for {artifact_value[:40]}.",
        )
