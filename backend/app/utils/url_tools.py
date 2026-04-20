"""
Purpose:
    URL normalization helpers for scan submissions and dedupe keys.
Inputs:
    Raw URL strings from user or organization submissions.
Outputs:
    Safer normalized URL strings for caching and enrichment calls.
Dependencies:
    Standard library `urllib.parse`.
TODO Checklist:
    - [ ] Add defanging helpers for UI display if reused by frontend tooling.
    - [ ] Add stronger validation for IDNs and suspicious encodings.
"""

from urllib.parse import quote, urlparse, urlunparse


def normalize_url(raw_url: str) -> str:
    """Normalize a URL enough for scaffold-level dedupe behavior."""
    candidate = raw_url.strip()
    if "://" not in candidate:
        candidate = f"https://{candidate}"

    parsed = urlparse(candidate)
    hostname = (parsed.hostname or "").lower()
    if not hostname:
        raise ValueError("URL artifacts must include a hostname.")

    scheme = (parsed.scheme or "https").lower()
    port = parsed.port
    if (scheme == "https" and port == 443) or (scheme == "http" and port == 80):
        port = None

    userinfo = ""
    if parsed.username:
        userinfo = parsed.username
        if parsed.password:
            userinfo = f"{userinfo}:{parsed.password}"
        userinfo = f"{userinfo}@"

    netloc = f"{userinfo}{hostname}"
    if port is not None:
        netloc = f"{netloc}:{port}"

    path = quote(parsed.path or "/", safe="/%:@")
    normalized = parsed._replace(
        scheme=scheme,
        netloc=netloc,
        path=path,
        params="",
        fragment="",
    )
    return urlunparse(normalized)
