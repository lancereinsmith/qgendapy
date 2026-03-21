from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class UserResource(BaseResource):
    """Synchronous user endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse:
        return self._get("/user", odata=odata)

    def get(self, user_key: str, *, odata: OData | None = None) -> QGendaResponse:
        return self._get(f"/user/{user_key}", odata=odata)

    def non_scheduled(self, *, odata: OData | None = None) -> QGendaResponse:
        return self._get("/NonScheduledUser", odata=odata)

    def non_scheduled_permissions(self, location_key: str) -> QGendaResponse:
        return self._get(f"/NonScheduledUser/location/{location_key}/permissions")


class AsyncUserResource(AsyncBaseResource):
    """Asynchronous user endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse:
        return await self._get("/user", odata=odata)

    async def get(self, user_key: str, *, odata: OData | None = None) -> QGendaResponse:
        return await self._get(f"/user/{user_key}", odata=odata)

    async def non_scheduled(self, *, odata: OData | None = None) -> QGendaResponse:
        return await self._get("/NonScheduledUser", odata=odata)

    async def non_scheduled_permissions(self, location_key: str) -> QGendaResponse:
        return await self._get(f"/NonScheduledUser/location/{location_key}/permissions")
