from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.facility import Facility
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class FacilityResource(BaseResource):
    """Synchronous facility / location endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[Facility]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        return self._get("/location", params=params, model=Facility, odata=odata)

    def create(self, *, data: dict) -> QGendaResponse[Facility]:
        return self._post("/location", json=data, model=Facility)

    def get(self, location_key: str, *, odata: OData | None = None) -> QGendaResponse[Facility]:
        return self._get(f"/location/{location_key}", model=Facility, odata=odata)

    def update(self, location_key: str, *, data: dict) -> QGendaResponse[Facility]:
        return self._put(f"/location/{location_key}", json=data, model=Facility)

    def delete(self, location_key: str) -> QGendaResponse:
        return self._delete(f"/location/{location_key}")

    def staff(self, location_key: str) -> QGendaResponse:
        return self._get(f"/location/{location_key}/staff")

    def add_staff(self, location_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/location/{location_key}/staff", json=data)

    def update_staff(self, location_key: str, staff_key: str, *, data: dict) -> QGendaResponse:
        return self._put(f"/location/{location_key}/staff/{staff_key}", json=data)

    def remove_staff(self, location_key: str, staff_key: str) -> QGendaResponse:
        return self._delete(f"/location/{location_key}/staff/{staff_key}")

    def staff_credentials(self, location_key: str, staff_key: str) -> QGendaResponse:
        return self._get(f"/location/{location_key}/staff/{staff_key}/credential")

    def staff_fte(self, location_key: str, staff_key: str) -> QGendaResponse:
        return self._get(f"/location/{location_key}/staff/{staff_key}/FTE")

    def update_staff_fte(self, location_key: str, staff_key: str, *, data: dict) -> QGendaResponse:
        return self._put(f"/location/{location_key}/staff/{staff_key}/FTE", json=data)

    def staff_tags(self, location_key: str, staff_key: str) -> QGendaResponse:
        return self._get(f"/location/{location_key}/staff/{staff_key}/tag")

    def update_staff_tag(self, location_key: str, staff_key: str, *, data: dict) -> QGendaResponse:
        return self._put(f"/location/{location_key}/staff/{staff_key}/tag", json=data)

    def tags(self, location_key: str) -> QGendaResponse:
        return self._get(f"/location/{location_key}/tag")

    def update_tag(self, location_key: str, *, data: dict) -> QGendaResponse:
        return self._put(f"/location/{location_key}/tag", json=data)

    def tasks(self, location_key: str) -> QGendaResponse:
        return self._get(f"/location/{location_key}/tasks")

    def add_task(self, location_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/location/{location_key}/task", json=data)

    def update_task(self, location_key: str, task_key: str, *, data: dict) -> QGendaResponse:
        return self._put(f"/location/{location_key}/task/{task_key}", json=data)

    def remove_task(self, location_key: str, task_key: str) -> QGendaResponse:
        return self._delete(f"/location/{location_key}/task/{task_key}")


class AsyncFacilityResource(AsyncBaseResource):
    """Asynchronous facility / location endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[Facility]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        return await self._get("/location", params=params, model=Facility, odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse[Facility]:
        return await self._post("/location", json=data, model=Facility)

    async def get(
        self, location_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[Facility]:
        return await self._get(f"/location/{location_key}", model=Facility, odata=odata)

    async def update(self, location_key: str, *, data: dict) -> QGendaResponse[Facility]:
        return await self._put(f"/location/{location_key}", json=data, model=Facility)

    async def delete(self, location_key: str) -> QGendaResponse:
        return await self._delete(f"/location/{location_key}")

    async def staff(self, location_key: str) -> QGendaResponse:
        return await self._get(f"/location/{location_key}/staff")

    async def add_staff(self, location_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/location/{location_key}/staff", json=data)

    async def update_staff(
        self, location_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse:
        return await self._put(f"/location/{location_key}/staff/{staff_key}", json=data)

    async def remove_staff(self, location_key: str, staff_key: str) -> QGendaResponse:
        return await self._delete(f"/location/{location_key}/staff/{staff_key}")

    async def staff_credentials(self, location_key: str, staff_key: str) -> QGendaResponse:
        return await self._get(f"/location/{location_key}/staff/{staff_key}/credential")

    async def staff_fte(self, location_key: str, staff_key: str) -> QGendaResponse:
        return await self._get(f"/location/{location_key}/staff/{staff_key}/FTE")

    async def update_staff_fte(
        self, location_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse:
        return await self._put(f"/location/{location_key}/staff/{staff_key}/FTE", json=data)

    async def staff_tags(self, location_key: str, staff_key: str) -> QGendaResponse:
        return await self._get(f"/location/{location_key}/staff/{staff_key}/tag")

    async def update_staff_tag(
        self, location_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse:
        return await self._put(f"/location/{location_key}/staff/{staff_key}/tag", json=data)

    async def tags(self, location_key: str) -> QGendaResponse:
        return await self._get(f"/location/{location_key}/tag")

    async def update_tag(self, location_key: str, *, data: dict) -> QGendaResponse:
        return await self._put(f"/location/{location_key}/tag", json=data)

    async def tasks(self, location_key: str) -> QGendaResponse:
        return await self._get(f"/location/{location_key}/tasks")

    async def add_task(self, location_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/location/{location_key}/task", json=data)

    async def update_task(self, location_key: str, task_key: str, *, data: dict) -> QGendaResponse:
        return await self._put(f"/location/{location_key}/task/{task_key}", json=data)

    async def remove_task(self, location_key: str, task_key: str) -> QGendaResponse:
        return await self._delete(f"/location/{location_key}/task/{task_key}")
