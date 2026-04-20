"""
Purpose:
    Normalize incoming artifacts before caching, IOC extraction, and enrichment.
Inputs:
    Raw artifact type and user-provided value.
Outputs:
    Normalized string representation safe for dedupe and downstream services.
Dependencies:
    URL/email helper utilities.
TODO Checklist:
    - [ ] Add stronger per-type validation and canonicalization rules.
    - [ ] Add MIME/attachment handling when raw email or file uploads are implemented.
"""

from app.utils.email_tools import normalize_email_signal
from app.utils.enums import ArtifactType
from app.utils.hashing import normalize_hash_value, sha256_text
from app.utils.url_tools import normalize_url


class NormalizationService:
    """Normalize scaffold artifact inputs in one reusable place."""

    def normalize(self, artifact_type: ArtifactType, raw_value: str) -> str:
        """
        Return a normalized artifact string based on its intake lane.

        This keeps the artifact-to-normalizer mapping easy to follow before any
        real validation or scan execution is introduced.
        """
        if artifact_type == ArtifactType.URL:
            return normalize_url(raw_value)
        if artifact_type == ArtifactType.EMAIL_SIGNAL:
            return normalize_email_signal(raw_value)
        if artifact_type == ArtifactType.HASH:
            return normalize_hash_value(raw_value)
        if artifact_type == ArtifactType.FILE:
            return sha256_text(raw_value.strip())
        return raw_value.strip().lower()
