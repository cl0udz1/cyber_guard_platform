"""
Purpose:
    In-memory cache placeholder for duplicate scan submission behavior.
Inputs:
    Cache keys from normalized artifacts and AI mode selections.
Outputs:
    Previously generated scan job responses.
Dependencies:
    Standard library dictionaries.
TODO Checklist:
    - [ ] Replace in-memory cache with Redis or DB-backed cache if needed.
    - [ ] Add cache invalidation and freshness rules once real enrichment is live.
"""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256

from app.schemas.scan import ScanJobResponse


@dataclass
class CachedScanEntry:
    """Stored scan response plus freshness metadata."""

    response: ScanJobResponse
    created_at: datetime
    expires_at: datetime


class CachingService:
    """Simple process-local cache with TTL support for scaffold demonstrations."""

    def __init__(
        self,
        ttl_seconds: int = 300,
        time_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self.ttl_seconds = max(ttl_seconds, 0)
        self._time_provider = time_provider or self._utc_now
        self._scan_cache: dict[str, CachedScanEntry] = {}

    def build_scan_key(self, artifact_type: str, artifact_value: str, ai_mode: str) -> str:
        """Build a stable cache key used to identify duplicate scaffold submissions."""
        raw_key = f"{artifact_type}:{artifact_value}:{ai_mode}"
        digest = sha256(raw_key.encode("utf-8")).hexdigest()
        return f"scan:{digest}"

    def get_scan(self, key: str) -> ScanJobResponse | None:
        """Return cached scan response if present."""
        entry = self._scan_cache.get(key)
        if entry is None:
            return None
        if self._is_expired(entry):
            self._scan_cache.pop(key, None)
            return None
        return entry.response

    def set_scan(self, key: str, response: ScanJobResponse) -> None:
        """Store a scan response by cache key."""
        created_at = self._now()
        expires_at = created_at + timedelta(seconds=self.ttl_seconds)
        self._scan_cache[key] = CachedScanEntry(
            response=response,
            created_at=created_at,
            expires_at=expires_at,
        )

    def evict_scan(self, key: str) -> bool:
        """Remove one cached scan response if present."""
        return self._scan_cache.pop(key, None) is not None

    def clear_expired(self) -> int:
        """Remove expired cache entries and return how many were cleared."""
        expired_keys = [
            key for key, entry in self._scan_cache.items() if self._is_expired(entry)
        ]
        for key in expired_keys:
            self._scan_cache.pop(key, None)
        return len(expired_keys)

    def cache_size(self) -> int:
        """Return the current number of fresh cached scan entries."""
        self.clear_expired()
        return len(self._scan_cache)

    def _is_expired(self, entry: CachedScanEntry) -> bool:
        """Return whether the cached scan response is no longer fresh."""
        return entry.expires_at <= self._now()

    def _now(self) -> datetime:
        """Return the current timezone-aware UTC timestamp."""
        current = self._time_provider()
        if current.tzinfo is None:
            return current.replace(tzinfo=timezone.utc)
        return current.astimezone(timezone.utc)

    @staticmethod
    def _utc_now() -> datetime:
        """Return the default current UTC timestamp."""
        return datetime.now(timezone.utc)
