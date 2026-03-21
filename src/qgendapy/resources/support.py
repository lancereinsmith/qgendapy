from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.response import QGendaResponse


class SupportResource(BaseResource):
    """Synchronous support endpoints."""

    def send_message(self, staff_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/support/staff/{staff_key}", json=data)


class AsyncSupportResource(AsyncBaseResource):
    """Asynchronous support endpoints."""

    async def send_message(self, staff_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/support/staff/{staff_key}", json=data)
