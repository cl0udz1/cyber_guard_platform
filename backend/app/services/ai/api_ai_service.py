"""
Purpose:
    Convenience-focused remote AI analysis mode using deterministic pre-send summaries.
Inputs:
    Artifact value, indicators, and source hits.
Outputs:
    API-mode AI summary text.
Dependencies:
    AI adapter protocol only.
TODO Checklist:
    - [ ] Add provider-specific request/response handling when implemented.
    - [ ] Add privacy redaction rules before sending data externally.
"""

from app.schemas.scan import SourceHit
from app.services.ai.base import (
    build_ai_summary,
    dominant_verdict,
    preview_artifact_value,
    recommended_action_for_verdict,
    summarize_verdict_mix,
)


class ApiAiService:
    """Remote AI summary builder intended for later provider integration."""

    def __init__(self, enabled: bool, provider_name: str) -> None:
        self.enabled = enabled
        self.provider_name = provider_name

    async def analyze(
        self,
        artifact_value: str,
        indicators: list[str],
        source_hits: list[SourceHit],
    ) -> str | None:
        """Return a deterministic API-mode summary."""
        if not self.enabled:
            return None
        dominant = dominant_verdict(source_hits)
        return build_ai_summary(
            mode_name="API",
            indicators_count=len(indicators),
            source_hits_count=len(source_hits),
            detail=(
                f"Artifact preview: '{preview_artifact_value(artifact_value)}'. "
                f"Current verdict mix before remote summarization: {summarize_verdict_mix(source_hits)}. "
                f"Configured provider: {self.provider_name}. "
                f"Recommended next step: {recommended_action_for_verdict(dominant)}"
            ),
        )
