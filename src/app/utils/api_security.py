"""API key security utilities."""

from __future__ import annotations

import hmac
import os
from hashlib import sha256

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv()

_UYD_API_KEY = os.getenv("UYD_API_KEY", "secret")


def _get_api_key() -> str:
    if not _UYD_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key is not configured",
        )
    return _UYD_API_KEY


def _digest(value: str) -> str:
    return hmac.new(value.encode(), digestmod=sha256).hexdigest()


async def verify_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    """Validate the provided API key header using constant-time comparison."""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    expected_key = _get_api_key()
    if not hmac.compare_digest(
        hmac.new(expected_key.encode(), digestmod=sha256).digest(),
        hmac.new(x_api_key.encode(), digestmod=sha256).digest(),
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
