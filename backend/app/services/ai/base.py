"""
Purpose:
    Shared interface for optional AI analysis adapters.
Inputs:
    Artifact value, extracted indicators, and source hit summaries.
Outputs:
    Optional analyst-friendly narrative text.
Dependencies:
    Standard library typing only.
TODO Checklist:
    - [ ] Add token budgeting and privacy guardrails before real integration.
"""

from collections import Counter
from typing import Protocol

from app.schemas.scan import SourceHit

_VERDICT_PRIORITY = {
    "informational": 1,
    "observed": 2,
    "suspicious": 3,
    "malicious": 4,
}


def build_ai_summary(
    mode_name: str,
    indicators_count: int,
    source_hits_count: int,
    detail: str,
) -> str:
    """Build a consistent scaffold summary for optional AI modes."""
    return (
        f"{mode_name} AI mode reviewed {indicators_count} indicators across "
        f"{source_hits_count} source results. {detail}"
    )


def dominant_verdict(source_hits: list[SourceHit]) -> str:
    """Return the highest-priority verdict present in the current source hits."""
    if not source_hits:
        return "informational"
    verdicts = {hit.verdict for hit in source_hits}
    return max(verdicts, key=lambda verdict: _VERDICT_PRIORITY.get(verdict, 0))


def highest_confidence_hit(source_hits: list[SourceHit]) -> SourceHit | None:
    """Return the strongest source hit for the current scan."""
    if not source_hits:
        return None
    return max(
        source_hits,
        key=lambda hit: (hit.confidence_score, _VERDICT_PRIORITY.get(hit.verdict, 0)),
    )


def summarize_verdict_mix(source_hits: list[SourceHit]) -> str:
    """Return a compact count summary of verdict types."""
    verdict_counts = Counter(hit.verdict for hit in source_hits)
    if not verdict_counts:
        return "no source verdicts"
    parts = [
        f"{verdict_counts[verdict]} {verdict}"
        for verdict in sorted(
            verdict_counts,
            key=lambda verdict: _VERDICT_PRIORITY.get(verdict, 0),
            reverse=True,
        )
    ]
    return ", ".join(parts)


def recommended_action_for_verdict(verdict: str) -> str:
    """Return the next-step guidance for the dominant verdict."""
    if verdict == "malicious":
        return "Contain the artifact, block related indicators, and escalate for analyst review."
    if verdict == "suspicious":
        return "Keep the artifact in the private workspace and validate the strongest source findings."
    if verdict == "observed":
        return "Monitor for repeated submissions and compare against trusted context before escalation."
    return "Keep the submission as reference telemetry unless stronger evidence appears."


def preview_artifact_value(artifact_value: str, limit: int = 60) -> str:
    """Return a readable artifact preview for summaries."""
    compact_value = " ".join(artifact_value.split())
    if len(compact_value) <= limit:
        return compact_value
    return f"{compact_value[: limit - 3]}..."


class AiAnalysisAdapter(Protocol):
    """Protocol for scaffold AI analysis services."""

    async def analyze(
        self,
        artifact_value: str,
        indicators: list[str],
        source_hits: list[SourceHit],
    ) -> str | None:
        """Return optional AI-generated narrative text."""
