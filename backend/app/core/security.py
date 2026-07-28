import time
from typing import Any

import httpx
from jose import jwt
from jose.exceptions import JOSEError

from app.core.settings import get_settings

_JWKS_CACHE_SECONDS = 3600
_jwks_cache: dict[str, Any] = {"keys": [], "fetched_at": 0.0}


def _fetch_jwks(issuer: str, *, force_refresh: bool = False) -> list[dict[str, Any]]:
    now = time.monotonic()
    if not force_refresh and _jwks_cache["keys"] and now - _jwks_cache["fetched_at"] < _JWKS_CACHE_SECONDS:
        return _jwks_cache["keys"]

    try:
        response = httpx.get(f"{issuer}/.well-known/jwks.json", timeout=5.0)
        response.raise_for_status()
        keys = response.json()["keys"]
    except (httpx.HTTPError, KeyError, ValueError) as error:
        raise ValueError("Unable to fetch Clerk signing keys") from error

    _jwks_cache["keys"] = keys
    _jwks_cache["fetched_at"] = now
    return keys


def verify_clerk_token(token: str) -> str:
    """Verify a Clerk session JWT against Clerk's JWKS and return the Clerk user id (`sub`)."""
    settings = get_settings()
    if not settings.clerk_issuer:
        raise ValueError("Clerk issuer is not configured")

    try:
        kid = jwt.get_unverified_header(token).get("kid")
    except JOSEError as error:
        raise ValueError("Invalid authentication token") from error

    keys = _fetch_jwks(settings.clerk_issuer)
    key = next((candidate for candidate in keys if candidate.get("kid") == kid), None)
    if key is None:
        # Key rotated since our last fetch — refresh once before giving up.
        keys = _fetch_jwks(settings.clerk_issuer, force_refresh=True)
        key = next((candidate for candidate in keys if candidate.get("kid") == kid), None)
    if key is None:
        raise ValueError("Invalid authentication token")

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=settings.clerk_issuer,
            options={"verify_aud": False},
        )
    except JOSEError as error:
        raise ValueError("Invalid authentication token") from error

    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise ValueError("Invalid authentication token")

    return subject
