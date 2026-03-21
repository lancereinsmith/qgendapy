from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.request import RequestLimit
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class RequestLimitResource(BaseResource):
    """Synchronous request limit endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[RequestLimit]:
        return self._get("/requestlimit", model=RequestLimit, odata=odata)

    def create(self, *, data: dict) -> QGendaResponse[RequestLimit]:
        return self._post("/requestlimit", json=data, model=RequestLimit)

    def update(self, request_limit_key: str, *, data: dict) -> QGendaResponse[RequestLimit]:
        return self._put(f"/requestlimit/{request_limit_key}", json=data, model=RequestLimit)

    def delete(self, request_limit_key: str) -> QGendaResponse:
        return self._delete(f"/requestlimit/{request_limit_key}")

    def staff_quotas(self, request_limit_key: str) -> QGendaResponse:
        return self._get(f"/requestlimit/{request_limit_key}/staffquota")

    def create_staff_quota(self, request_limit_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/requestlimit/{request_limit_key}/staffquota", json=data)

    def update_staff_quota(
        self, request_limit_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse:
        return self._put(f"/requestlimit/{request_limit_key}/staffquota/{staff_key}", json=data)

    def task_shifts(self, request_limit_key: str) -> QGendaResponse:
        return self._get(f"/requestlimit/{request_limit_key}/taskshift")

    def create_task_shift(self, request_limit_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/requestlimit/{request_limit_key}/taskshift", json=data)

    def update_task_shift(
        self, request_limit_key: str, task_shift_key: str, *, data: dict
    ) -> QGendaResponse:
        return self._put(
            f"/requestlimit/{request_limit_key}/taskshift/{task_shift_key}",
            json=data,
        )

    def delete_task_shift(self, request_limit_key: str, task_shift_key: str) -> QGendaResponse:
        return self._delete(f"/requestlimit/{request_limit_key}/taskshift/{task_shift_key}")


class AsyncRequestLimitResource(AsyncBaseResource):
    """Asynchronous request limit endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[RequestLimit]:
        return await self._get("/requestlimit", model=RequestLimit, odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse[RequestLimit]:
        return await self._post("/requestlimit", json=data, model=RequestLimit)

    async def update(self, request_limit_key: str, *, data: dict) -> QGendaResponse[RequestLimit]:
        return await self._put(f"/requestlimit/{request_limit_key}", json=data, model=RequestLimit)

    async def delete(self, request_limit_key: str) -> QGendaResponse:
        return await self._delete(f"/requestlimit/{request_limit_key}")

    async def staff_quotas(self, request_limit_key: str) -> QGendaResponse:
        return await self._get(f"/requestlimit/{request_limit_key}/staffquota")

    async def create_staff_quota(self, request_limit_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/requestlimit/{request_limit_key}/staffquota", json=data)

    async def update_staff_quota(
        self, request_limit_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse:
        return await self._put(
            f"/requestlimit/{request_limit_key}/staffquota/{staff_key}", json=data
        )

    async def task_shifts(self, request_limit_key: str) -> QGendaResponse:
        return await self._get(f"/requestlimit/{request_limit_key}/taskshift")

    async def create_task_shift(self, request_limit_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/requestlimit/{request_limit_key}/taskshift", json=data)

    async def update_task_shift(
        self, request_limit_key: str, task_shift_key: str, *, data: dict
    ) -> QGendaResponse:
        return await self._put(
            f"/requestlimit/{request_limit_key}/taskshift/{task_shift_key}",
            json=data,
        )

    async def delete_task_shift(
        self, request_limit_key: str, task_shift_key: str
    ) -> QGendaResponse:
        return await self._delete(f"/requestlimit/{request_limit_key}/taskshift/{task_shift_key}")
