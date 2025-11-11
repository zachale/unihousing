import json
from typing import Any

def stable_stringify(data: Any) -> str:
    """
    Deterministic JSON serialization:
    - sorts keys for objects
    - removes extra whitespace
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

def fnv1a_32(text: str) -> int:
    """
    32-bit FNV-1a hash -> returns unsigned 32-bit integer
    Order-sensitive: even one character difference changes the checksum.
    """
    FNV_PRIME = 0x01000193
    hash_val = 0x811C9DC5  # offset basis

    for char in text:
        hash_val ^= ord(char)
        hash_val = (hash_val * FNV_PRIME) % (2 ** 32)

    return hash_val

def json_checksum(data: Any) -> int:
    """
    Compute a deterministic unsigned 32-bit checksum for a JSON-serializable object.
    """
    canonical = stable_stringify(data)
    return fnv1a_32(canonical)

def string_checksum(s: str) -> int:
    """
    Compute a deterministic unsigned 32-bit checksum for a string.
    Order matters: even one character change produces a different checksum.
    """
    return fnv1a_32(s)
