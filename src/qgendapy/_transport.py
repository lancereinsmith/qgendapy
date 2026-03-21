from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from qgendapy._auth import AsyncAuth, Auth


class Transport:
    """Synchronous HTTP transport wrapping httpx.Client."""

    def __init__(self, auth: Auth, base_url: str) -> None:
        self._auth = auth
        self._base_url = base_url
        self._client = httpx.Client(base_url=base_url)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        json: dict | list | None = None,
        data: dict | None = None,
        files: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        merged_headers = {**(headers or {}), "Authorization": f"Bearer {self._auth.token}"}
        return self._client.request(
            method,
            path,
            params=params,
            json=json,
            data=data,
            files=files,
            headers=merged_headers,
        )

    def close(self) -> None:
        self._client.close()


class AsyncTransport:
    """Asynchronous HTTP transport wrapping httpx.AsyncClient."""

    def __init__(self, auth: AsyncAuth, base_url: str) -> None:
        self._auth = auth
        self._base_url = base_url
        self._client = httpx.AsyncClient(base_url=base_url)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        json: dict | list | None = None,
        data: dict | None = None,
        files: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        token = await self._auth.get_token()
        merged_headers = {**(headers or {}), "Authorization": f"Bearer {token}"}
        return await self._client.request(
            method,
            path,
            params=params,
            json=json,
            data=data,
            files=files,
            headers=merged_headers,
        )

    async def close(self) -> None:
        await self._client.aclose()
