"""
Purpose:
    Privacy-preserving local AI analysis mode using deterministic source summarization.
Inputs:
    Artifact value, indicators, and source hits.
Outputs:
    Local analyst summary text derived from source results.
Dependencies:
    AI adapter helpers only.
TODO Checklist:
    - [ ] Replace deterministic summaries with a real local model invocation if selected.
"""

from app.schemas.scan import SourceHit
from app.services.ai.base import (
    build_ai_summary,
    dominant_verdict,
    highest_confidence_hit,
    preview_artifact_value,
    recommended_action_for_verdict,
    summarize_verdict_mix,
)


class LocalAiService:
    """Local AI summarizer that never leaves the environment."""

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    async def analyze(
        self,
        artifact_value: str,
        indicators: list[str],
        source_hits: list[SourceHit],
    ) -> str | None:
        """Return a deterministic local-mode analyst summary."""
        if not self.enabled:
            return None

        dominant = dominant_verdict(source_hits)
        top_hit = highest_confidence_hit(source_hits)
        indicator_preview = self._indicator_preview(indicators)
        artifact_preview = preview_artifact_value(artifact_value)

        if top_hit is None:
            detail = (
                f"Artifact preview: '{artifact_preview}'. "
                "No enrichment source returned a result yet. "
                "Recommended next step: keep the submission queued for analyst review."
            )
            return build_ai_summary(
                mode_name="Local",
                indicators_count=len(indicators),
                source_hits_count=0,
                detail=detail,
            )

        return build_ai_summary(
            mode_name="Local",
            indicators_count=len(indicators),
            source_hits_count=len(source_hits),
            detail=(
                f"Artifact preview: '{artifact_preview}'. "
                f"Dominant verdict: {dominant}. "
                f"Verdict mix: {summarize_verdict_mix(source_hits)}. "
                f"Highest-confidence source: {top_hit.source_name} ({top_hit.confidence_score}/100). "
                f"Indicator sample: {indicator_preview}. "
                f"Recommended next step: {recommended_action_for_verdict(dominant)}"
            ),
        )

    def _indicator_preview(self, indicators: list[str]) -> str:
        """Return a compact indicator preview for analyst summaries."""
        cleaned_indicators = [indicator.strip() for indicator in indicators if indicator.strip()]
        if not cleaned_indicators:
            return "none"
        preview = ", ".join(cleaned_indicators[:3])
        if len(cleaned_indicators) > 3:
            return f"{preview}, ..."
        return preview
