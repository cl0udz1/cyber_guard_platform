"""
Purpose:
    Lightweight helpers for pasted email indicator handling.
Inputs:
    Email addresses, subjects, or pasted email snippets from submissions.
Outputs:
    Normalized email-related values suitable for IOC extraction.
Dependencies:
    Standard library string helpers.
TODO Checklist:
    - [ ] Add MIME parsing if raw `.eml` upload support becomes part of the MVP.
    - [ ] Add domain extraction and sender/recipient field parsing.
"""

import re

EMAIL_PATTERN = re.compile(r"\b[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}\b")
URL_PATTERN = re.compile(r"\bhttps?://[^\s<>\"]+\b")
DOMAIN_PATTERN = re.compile(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b")


def normalize_email_signal(raw_value: str) -> str:
    """Collapse whitespace and lowercase email-signal content for consistent matching."""
    return " ".join(raw_value.strip().split()).lower()


def extract_email_indicators(normalized_value: str) -> list[str]:
    """Extract a small deduplicated IOC set from normalized email-signal content."""
    indicators: list[str] = []

    for pattern in (EMAIL_PATTERN, URL_PATTERN, DOMAIN_PATTERN):
        for match in pattern.findall(normalized_value):
            if match not in indicators:
                indicators.append(match)

    return indicators
