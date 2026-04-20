"""
Purpose:
    Local VirusTotal-style adapter that scores artifacts without calling the network.
Inputs:
    Extracted indicators and normalized artifact values.
Outputs:
    Per-source verdict summary for the scan orchestrator.
Dependencies:
    Adapter protocol, URL parsing, and local heuristic rules.
TODO Checklist:
    - [ ] Replace local heuristics with real HTTP requests and parsing when ready.
    - [ ] Add timeout, rate limit, and retry handling once integrated.
"""

import re
from ipaddress import ip_address
from urllib.parse import parse_qsl, urlparse

from app.services.enrichment.base import (
    EnrichmentHitPayload,
    build_enrichment_hit_payload,
)


class VirusTotalClient:
    """Threat-intel adapter with local heuristic scoring for VirusTotal-style results."""

    _KEYWORD_WEIGHTS = {
        "account": 8,
        "confirm": 7,
        "invoice": 6,
        "login": 12,
        "password": 12,
        "reset": 9,
        "secure": 5,
        "signin": 12,
        "token": 8,
        "update": 7,
        "urgent": 5,
        "verify": 10,
        "wallet": 11,
    }
    _TRACKING_KEYS = {"auth", "continue", "email", "next", "redirect", "session", "token"}
    _HASH_PATTERN = re.compile(r"^[a-f0-9]{32}$|^[a-f0-9]{40}$|^[a-f0-9]{64}$")

    name = "virustotal"

    def __init__(self, api_key: str, base_url: str, timeout_seconds: int) -> None:
        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = max(timeout_seconds, 1)

    async def enrich(
        self,
        indicators: list[str],
        artifact_value: str,
    ) -> EnrichmentHitPayload:
        """Return a deterministic local assessment without calling the network."""
        unique_indicators = self._unique_indicators(indicators, artifact_value)
        confidence_score, reasons, subject = self._score_artifact(artifact_value, unique_indicators)
        verdict = self._verdict_from_score(confidence_score)
        return build_enrichment_hit_payload(
            source_name=self.name,
            verdict=verdict,
            confidence_score=confidence_score,
            summary=self._build_summary(subject, verdict, confidence_score, reasons),
        )

    def _score_artifact(
        self,
        artifact_value: str,
        indicators: list[str],
    ) -> tuple[int, list[str], str]:
        """Score the artifact with lightweight local heuristics."""
        score = 22
        reasons: list[str] = []
        lowered_value = artifact_value.lower()
        parsed = urlparse(artifact_value)
        subject = self._preview_subject(parsed.hostname or artifact_value)

        if parsed.scheme and parsed.netloc:
            if parsed.scheme == "http":
                score += 14
                reasons.append("plain HTTP transport")

            host = parsed.hostname or ""
            if host:
                if self._is_ip_host(host):
                    score += 18
                    reasons.append("direct IP host")
                if host.startswith("xn--"):
                    score += 12
                    reasons.append("punycode hostname")
                if host.count(".") >= 3:
                    score += 4
                    reasons.append("deep subdomain chain")

            query_params = parse_qsl(parsed.query, keep_blank_values=True)
            if len(query_params) >= 3:
                score += 8
                reasons.append("multiple query parameters")
            if any(name.lower() in self._TRACKING_KEYS for name, _ in query_params):
                score += 8
                reasons.append("tracking or redirect parameters")

        keyword_hits = [keyword for keyword in self._KEYWORD_WEIGHTS if keyword in lowered_value]
        if keyword_hits:
            score += min(26, sum(self._KEYWORD_WEIGHTS[keyword] for keyword in keyword_hits[:3]))
            reasons.append(f"credential-themed keywords ({', '.join(keyword_hits[:3])})")

        if len(indicators) >= 3:
            score += 6
            reasons.append(f"{len(indicators)} correlated indicators")
        elif len(indicators) == 2:
            score += 3
            reasons.append("multiple correlated indicators")

        if self._looks_like_hash(artifact_value):
            score = max(score, 38)
            reasons.append("hash-style lookup artifact")

        return max(15, min(score, 95)), reasons[:3], subject

    def _build_summary(
        self,
        subject: str,
        verdict: str,
        confidence_score: int,
        reasons: list[str],
    ) -> str:
        """Create a short analyst-readable summary for the orchestrator."""
        if reasons:
            reason_text = ", ".join(reasons)
        else:
            reason_text = "limited matching telemetry in the local heuristic pass"
        return (
            f"VirusTotal-style local assessment marked {subject} as {verdict} "
            f"({confidence_score}/100) based on {reason_text}."
        )

    def _unique_indicators(self, indicators: list[str], artifact_value: str) -> list[str]:
        """Return de-duplicated indicators while always including the artifact itself."""
        unique_indicators: list[str] = []
        for candidate in [artifact_value, *indicators]:
            normalized = candidate.strip()
            if normalized and normalized not in unique_indicators:
                unique_indicators.append(normalized)
        return unique_indicators

    @classmethod
    def _verdict_from_score(cls, confidence_score: int) -> str:
        """Map a local heuristic score into the shared verdict vocabulary."""
        if confidence_score >= 85:
            return "malicious"
        if confidence_score >= 60:
            return "suspicious"
        if confidence_score >= 35:
            return "observed"
        return "informational"

    @classmethod
    def _looks_like_hash(cls, artifact_value: str) -> bool:
        """Return whether the artifact resembles a common hash length."""
        return bool(cls._HASH_PATTERN.fullmatch(artifact_value.lower()))

    @staticmethod
    def _is_ip_host(host: str) -> bool:
        """Return whether the host is a literal IP address."""
        try:
            ip_address(host)
        except ValueError:
            return False
        return True

    @staticmethod
    def _preview_subject(subject: str) -> str:
        """Return a compact subject string for summaries."""
        if len(subject) <= 48:
            return subject
        return f"{subject[:45]}..."
