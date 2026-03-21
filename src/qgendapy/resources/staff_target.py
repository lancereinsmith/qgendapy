from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class StaffTargetResource(BaseResource):
    """Synchronous staff target endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse:
        return self._get("/stafftarget", odata=odata)

    def create(self, *, data: dict) -> QGendaResponse:
        return self._post("/stafftarget", json=data)

    def update(self, *, data: dict) -> QGendaResponse:
        return self._put("/stafftarget", json=data)

    def delete(self, *, data: dict) -> QGendaResponse:
        return self._delete("/stafftarget", json=data)

    def locations(self, staff_target_key: str) -> QGendaResponse:
        return self._get(f"/stafftarget/{staff_target_key}/location")

    def add_location(self, staff_target_key: str, location_key: str) -> QGendaResponse:
        return self._post(f"/stafftarget/{staff_target_key}/location/{location_key}")

    def remove_location(self, staff_target_key: str, location_key: str) -> QGendaResponse:
        return self._delete(f"/stafftarget/{staff_target_key}/location/{location_key}")

    def profiles(self, staff_target_key: str) -> QGendaResponse:
        return self._get(f"/stafftarget/{staff_target_key}/profile")

    def staff(self, staff_target_key: str) -> QGendaResponse:
        return self._get(f"/stafftarget/{staff_target_key}/staff")

    def add_staff(
        self, staff_target_key: str, staff_key: str, *, data: dict | None = None
    ) -> QGendaResponse:
        return self._post(f"/stafftarget/{staff_target_key}/staff/{staff_key}", json=data)

    def update_staff(self, staff_target_key: str, staff_key: str, *, data: dict) -> QGendaResponse:
        return self._put(f"/stafftarget/{staff_target_key}/staff/{staff_key}", json=data)

    def remove_staff(self, staff_target_key: str, staff_key: str) -> QGendaResponse:
        return self._delete(f"/stafftarget/{staff_target_key}/staff/{staff_key}")

    def task_shifts(self, staff_target_key: str) -> QGendaResponse:
        return self._get(f"/stafftarget/{staff_target_key}/taskshift")

    def add_task_shift(self, staff_target_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/stafftarget/{staff_target_key}/taskshift", json=data)

    def remove_task_shift(self, staff_target_key: str, task_shift_key: str) -> QGendaResponse:
        return self._delete(f"/stafftarget/{staff_target_key}/taskshift/{task_shift_key}")


class AsyncStaffTargetResource(AsyncBaseResource):
    """Asynchronous staff target endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse:
        return await self._get("/stafftarget", odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse:
        return await self._post("/stafftarget", json=data)

    async def update(self, *, data: dict) -> QGendaResponse:
        return await self._put("/stafftarget", json=data)

    async def delete(self, *, data: dict) -> QGendaResponse:
        return await self._delete("/stafftarget", json=data)

    async def locations(self, staff_target_key: str) -> QGendaResponse:
        return await self._get(f"/stafftarget/{staff_target_key}/location")

    async def add_location(self, staff_target_key: str, location_key: str) -> QGendaResponse:
        return await self._post(f"/stafftarget/{staff_target_key}/location/{location_key}")

    async def remove_location(self, staff_target_key: str, location_key: str) -> QGendaResponse:
        return await self._delete(f"/stafftarget/{staff_target_key}/location/{location_key}")

    async def profiles(self, staff_target_key: str) -> QGendaResponse:
        return await self._get(f"/stafftarget/{staff_target_key}/profile")

    async def staff(self, staff_target_key: str) -> QGendaResponse:
        return await self._get(f"/stafftarget/{staff_target_key}/staff")

    async def add_staff(
        self, staff_target_key: str, staff_key: str, *, data: dict | None = None
    ) -> QGendaResponse:
        return await self._post(f"/stafftarget/{staff_target_key}/staff/{staff_key}", json=data)

    async def update_staff(
        self, staff_target_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse:
        return await self._put(f"/stafftarget/{staff_target_key}/staff/{staff_key}", json=data)

    async def remove_staff(self, staff_target_key: str, staff_key: str) -> QGendaResponse:
        return await self._delete(f"/stafftarget/{staff_target_key}/staff/{staff_key}")

    async def task_shifts(self, staff_target_key: str) -> QGendaResponse:
        return await self._get(f"/stafftarget/{staff_target_key}/taskshift")

    async def add_task_shift(self, staff_target_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/stafftarget/{staff_target_key}/taskshift", json=data)

    async def remove_task_shift(
        self, staff_target_key: str, task_shift_key: str
    ) -> QGendaResponse:
        return await self._delete(f"/stafftarget/{staff_target_key}/taskshift/{task_shift_key}")
