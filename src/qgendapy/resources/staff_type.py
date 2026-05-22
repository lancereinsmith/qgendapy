from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.staff import StaffType
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class StaffTypeResource(BaseResource):
    """Synchronous staff-type endpoints.

    Resolves ``StaffMember.staff_type_key`` to a human-readable name
    ("Shareholder", "Locum", "Staff", "Associate", etc.) shown in QGenda's
    Settings UI "Staff Type" column.
    """

    def list(self, *, odata: OData | None = None) -> QGendaResponse[StaffType]:
        return self._get("/stafftype", model=StaffType, odata=odata)


class AsyncStaffTypeResource(AsyncBaseResource):
    """Asynchronous staff-type endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[StaffType]:
        return await self._get("/stafftype", model=StaffType, odata=odata)
