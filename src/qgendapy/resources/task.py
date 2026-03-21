from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.task import Task, TaskShift
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class TaskResource(BaseResource):
    """Synchronous task endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[Task]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        return self._get("/task", params=params, model=Task, odata=odata)

    def create(self, *, data: dict) -> QGendaResponse[Task]:
        return self._post("/task", json=data, model=Task)

    def update(self, *, data: dict) -> QGendaResponse[Task]:
        return self._put("/task", json=data, model=Task)

    def locations(self, task_key: str) -> QGendaResponse:
        return self._get(f"/task/{task_key}/location")

    def tags(self, task_key: str) -> QGendaResponse:
        return self._get(f"/task/{task_key}/tag")

    def add_tag(self, task_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/task/{task_key}/tag", json=data)

    def shifts(self, task_key: str) -> QGendaResponse[TaskShift]:
        return self._get(f"/task/{task_key}/taskshift", model=TaskShift)

    def create_shift(self, task_key: str, *, data: dict) -> QGendaResponse[TaskShift]:
        return self._post(f"/task/{task_key}/taskshift", json=data, model=TaskShift)

    def update_shift(
        self, task_key: str, shift_key: str, *, data: dict
    ) -> QGendaResponse[TaskShift]:
        return self._put(f"/task/{task_key}/taskshift/{shift_key}", json=data, model=TaskShift)

    def delete_shift(self, task_key: str, shift_key: str) -> QGendaResponse:
        return self._delete(f"/task/{task_key}/taskshift/{shift_key}")


class AsyncTaskResource(AsyncBaseResource):
    """Asynchronous task endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[Task]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        return await self._get("/task", params=params, model=Task, odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse[Task]:
        return await self._post("/task", json=data, model=Task)

    async def update(self, *, data: dict) -> QGendaResponse[Task]:
        return await self._put("/task", json=data, model=Task)

    async def locations(self, task_key: str) -> QGendaResponse:
        return await self._get(f"/task/{task_key}/location")

    async def tags(self, task_key: str) -> QGendaResponse:
        return await self._get(f"/task/{task_key}/tag")

    async def add_tag(self, task_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/task/{task_key}/tag", json=data)

    async def shifts(self, task_key: str) -> QGendaResponse[TaskShift]:
        return await self._get(f"/task/{task_key}/taskshift", model=TaskShift)

    async def create_shift(self, task_key: str, *, data: dict) -> QGendaResponse[TaskShift]:
        return await self._post(f"/task/{task_key}/taskshift", json=data, model=TaskShift)

    async def update_shift(
        self, task_key: str, shift_key: str, *, data: dict
    ) -> QGendaResponse[TaskShift]:
        return await self._put(
            f"/task/{task_key}/taskshift/{shift_key}", json=data, model=TaskShift
        )

    async def delete_shift(self, task_key: str, shift_key: str) -> QGendaResponse:
        return await self._delete(f"/task/{task_key}/taskshift/{shift_key}")
