"""Text helpers used across handlers and services."""

from __future__ import annotations

from urllib.parse import urlparse


def is_url(value: str) -> bool:
    """Return True when the provided string looks like an HTTP(S) URL."""

    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def shorten_text(value: str, limit: int = 60) -> str:
    """Trim long text for compact UI previews."""

    value = value.strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"