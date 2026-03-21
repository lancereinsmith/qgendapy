from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from qgendapy.response import QGendaResponse

if TYPE_CHECKING:
    from qgendapy.client import AsyncQGendaClient, QGendaClient
    from qgendapy.odata import OData

T = TypeVar("T")


class BaseResource:
    """Base class for synchronous resource endpoints."""

    def __init__(self, client: QGendaClient) -> None:
        self._client = client

    def _get(
        self,
        path: str,
        *,
        params: dict | None = None,
        model: type[T] | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[T]:
        all_params = {**(params or {})}
        if odata:
            all_params.update(odata.to_params())
        resp = self._client._transport.request("GET", path, params=all_params)
        return QGendaResponse.from_httpx(resp, model=model)

    def _post(
        self,
        path: str,
        *,
        json: dict | list | None = None,
        params: dict | None = None,
        data: dict | None = None,
        files: dict | None = None,
        model: type[T] | None = None,
    ) -> QGendaResponse[T]:
        resp = self._client._transport.request(
            "POST", path, json=json, params=params, data=data, files=files
        )
        return QGendaResponse.from_httpx(resp, model=model)

    def _put(
        self,
        path: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
        model: type[T] | None = None,
    ) -> QGendaResponse[T]:
        resp = self._client._transport.request("PUT", path, json=json, params=params)
        return QGendaResponse.from_httpx(resp, model=model)

    def _delete(
        self,
        path: str,
        *,
        json: dict | list | None = None,
        params: dict | None = None,
    ) -> QGendaResponse:
        resp = self._client._transport.request("DELETE", path, json=json, params=params)
        return QGendaResponse.from_httpx(resp)


class AsyncBaseResource:
    """Base class for asynchronous resource endpoints."""

    def __init__(self, client: AsyncQGendaClient) -> None:
        self._client = client

    async def _get(
        self,
        path: str,
        *,
        params: dict | None = None,
        model: type[T] | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[T]:
        all_params = {**(params or {})}
        if odata:
            all_params.update(odata.to_params())
        resp = await self._client._transport.request("GET", path, params=all_params)
        return QGendaResponse.from_httpx(resp, model=model)

    async def _post(
        self,
        path: str,
        *,
        json: dict | list | None = None,
        params: dict | None = None,
        data: dict | None = None,
        files: dict | None = None,
        model: type[T] | None = None,
    ) -> QGendaResponse[T]:
        resp = await self._client._transport.request(
            "POST", path, json=json, params=params, data=data, files=files
        )
        return QGendaResponse.from_httpx(resp, model=model)

    async def _put(
        self,
        path: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
        model: type[T] | None = None,
    ) -> QGendaResponse[T]:
        resp = await self._client._transport.request("PUT", path, json=json, params=params)
        return QGendaResponse.from_httpx(resp, model=model)

    async def _delete(
        self,
        path: str,
        *,
        json: dict | list | None = None,
        params: dict | None = None,
    ) -> QGendaResponse:
        resp = await self._client._transport.request("DELETE", path, json=json, params=params)
        return QGendaResponse.from_httpx(resp)
