"""
Purpose:
    Hashing helpers for artifact normalization, cache keys, and report fingerprints.
Inputs:
    File bytes, byte chunks, or normalized text values.
Outputs:
    Hex digest strings safe to use as identifiers and dedupe keys.
Dependencies:
    Standard library `hashlib`.
TODO Checklist:
    - [ ] Add tests for stream/file object hashing helper.
    - [ ] Add alternate algorithms only if a real requirement appears.
"""

import hashlib
import re
from collections.abc import Iterable

HEX_DIGEST_PATTERN = re.compile(r"^[0-9a-fA-F]+$")
SUPPORTED_HASH_LENGTHS = {
    32: "md5",
    40: "sha1",
    64: "sha256",
}


def sha256_bytes(data: bytes) -> str:
    """Return SHA-256 hex digest for a byte sequence."""
    return hashlib.sha256(data).hexdigest()


def sha256_chunks(chunks: Iterable[bytes]) -> str:
    """
    Hash a stream of byte chunks.

    Useful for large-file processing without loading all bytes in memory.
    """
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    """Hash already-normalized text values such as URLs or pasted email signals."""
    return sha256_bytes(value.encode("utf-8"))


def is_supported_hash(value: str) -> bool:
    """Return whether the value looks like a supported hex digest."""
    candidate = value.strip()
    return len(candidate) in SUPPORTED_HASH_LENGTHS and bool(HEX_DIGEST_PATTERN.fullmatch(candidate))


def normalize_hash_value(value: str) -> str:
    """Return a lowercase normalized hash value or raise if the shape is unsupported."""
    candidate = value.strip().lower()
    if not is_supported_hash(candidate):
        raise ValueError("Hash artifacts must be MD5, SHA-1, or SHA-256 hex digests.")
    return candidate


def detect_hash_algorithm(value: str) -> str:
    """Return the inferred algorithm name for a supported hash digest."""
    normalized = normalize_hash_value(value)
    return SUPPORTED_HASH_LENGTHS[len(normalized)]
