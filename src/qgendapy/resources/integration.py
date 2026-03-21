from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.response import QGendaResponse


class IntegrationResource(BaseResource):
    """Synchronous integration endpoints."""

    def upload_file(
        self,
        *,
        files: dict,
        data: dict | None = None,
    ) -> QGendaResponse:
        return self._post("/Integration/File", files=files, data=data)


class AsyncIntegrationResource(AsyncBaseResource):
    """Asynchronous integration endpoints."""

    async def upload_file(
        self,
        *,
        files: dict,
        data: dict | None = None,
    ) -> QGendaResponse:
        return await self._post("/Integration/File", files=files, data=data)
