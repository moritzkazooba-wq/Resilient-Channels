import hashlib


def hash_phone(phone: str, salt: str) -> str:
    """SHA-256 of phone+salt, hex digest truncated to 16 chars."""
    return hashlib.sha256((phone + salt).encode()).hexdigest()[:16]
