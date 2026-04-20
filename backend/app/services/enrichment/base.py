"""
Purpose:
    Shared interface for threat-intel enrichment adapter placeholders.
Inputs:
    Extracted indicators and normalized artifact values.
Outputs:
    Consistent dictionaries that can become `SourceHit` models.
Dependencies:
    Standard library typing only.
TODO Checklist:
    - [ ] Replace scaffold payloads with richer adapter response models if needed.
    - [ ] Add standardized error/result metadata before real adapter implementation.
"""

from typing import Protocol, TypedDict


class EnrichmentHitPayload(TypedDict):
    """Shared scaffold payload returned by enrichment adapters."""

    source_name: str
    verdict: str
    confidence_score: int
    summary: str


def build_enrichment_hit_payload(
    source_name: str,
    verdict: str,
    confidence_score: int,
    summary: str,
) -> EnrichmentHitPayload:
    """Build the consistent placeholder shape expected by the orchestrator."""
    return {
        "source_name": source_name,
        "verdict": verdict,
        "confidence_score": confidence_score,
        "summary": summary,
    }


class EnrichmentAdapter(Protocol):
    """Protocol for scaffold enrichment clients."""

    name: str

    async def enrich(
        self,
        indicators: list[str],
        artifact_value: str,
    ) -> EnrichmentHitPayload:
        """Return source summary data for a scan request."""
