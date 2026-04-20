"""
Purpose:
    Extract IOC-like values from normalized artifacts.
Inputs:
    Normalized artifact value and artifact type.
Outputs:
    Small list of indicators that enrichment adapters can consume.
Dependencies:
    Scaffold enums only.
TODO Checklist:
    - [ ] Add regex-based extraction for URLs, domains, hashes, and email headers.
    - [ ] Separate extractor modules if email parsing becomes a real feature.
"""

from app.utils.enums import ArtifactType
from app.utils.email_tools import extract_email_indicators
from app.utils.url_tools import normalize_url


class IocExtractionService:
    """Return lightweight extracted indicators for the scaffold pipeline."""

    def extract(self, artifact_type: ArtifactType, normalized_value: str) -> list[str]:
        """Extract a small, predictable set of indicators for downstream stubs."""
        if artifact_type == ArtifactType.URL:
            parsed_url = normalize_url(normalized_value)
            hostname = parsed_url.split("://", maxsplit=1)[-1].split("/", maxsplit=1)[0]
            return [parsed_url, hostname]
        if artifact_type == ArtifactType.EMAIL_SIGNAL:
            return extract_email_indicators(normalized_value) or [normalized_value]
        return [normalized_value]
