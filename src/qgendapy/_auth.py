from __future__ import annotations

import asyncio
import threading
import time

import httpx

from qgendapy.exceptions import AuthenticationError


class Auth:
    """Synchronous token manager with auto-refresh.

    Thread-safe: uses a threading.Lock to protect token refresh.
    """

    _BUFFER_SECONDS = 60

    def __init__(self, email: str, password: str, base_url: str) -> None:
        self._email = email
        self._password = password
        self._login_url = f"{base_url}/login"
        self._access_token: str | None = None
        self._expires_at: float = 0.0
        self._lock = threading.Lock()

    @property
    def token(self) -> str:
        """Return current bearer token, refreshing if expired or absent."""
        with self._lock:
            if self._access_token is None or time.monotonic() >= self._expires_at:
                self._refresh()
            assert self._access_token is not None
            return self._access_token

    def _refresh(self) -> None:
        """POST to the login endpoint and store the new token."""
        with httpx.Client() as client:
            resp = client.post(
                self._login_url,
                data={"email": self._email, "password": self._password},
            )
        if resp.status_code != 200:
            raise AuthenticationError(f"Login failed with status {resp.status_code}: {resp.text}")

        body = resp.json()
        self._access_token = body["access_token"]
        expires_in = int(body.get("expires_in", 3600))
        self._expires_at = time.monotonic() + expires_in - self._BUFFER_SECONDS


class AsyncAuth:
    """Asynchronous token manager with auto-refresh.

    Uses asyncio.Lock to serialise concurrent refresh attempts.
    """

    _BUFFER_SECONDS = 60

    def __init__(self, email: str, password: str, base_url: str) -> None:
        self._email = email
        self._password = password
        self._login_url = f"{base_url}/login"
        self._access_token: str | None = None
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

    async def get_token(self) -> str:
        """Return current bearer token, refreshing if expired or absent."""
        async with self._lock:
            if self._access_token is None or time.monotonic() >= self._expires_at:
                await self._refresh()
            assert self._access_token is not None
            return self._access_token

    async def _refresh(self) -> None:
        """POST to the login endpoint and store the new token."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self._login_url,
                data={"email": self._email, "password": self._password},
            )
        if resp.status_code != 200:
            raise AuthenticationError(f"Login failed with status {resp.status_code}: {resp.text}")

        body = resp.json()
        self._access_token = body["access_token"]
        expires_in = int(body.get("expires_in", 3600))
        self._expires_at = time.monotonic() + expires_in - self._BUFFER_SECONDS
