from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.company import Company
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class CompanyResource(BaseResource):
    """Synchronous company endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[Company]:
        return self._get("/company", model=Company, odata=odata)


class AsyncCompanyResource(AsyncBaseResource):
    """Asynchronous company endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[Company]:
        return await self._get("/company", model=Company, odata=odata)
