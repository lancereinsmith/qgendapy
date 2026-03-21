from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.organization import Organization
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class OrganizationResource(BaseResource):
    """Synchronous organization endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[Organization]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        return self._get("/organization", params=params, model=Organization, odata=odata)


class AsyncOrganizationResource(AsyncBaseResource):
    """Asynchronous organization endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[Organization]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        return await self._get("/organization", params=params, model=Organization, odata=odata)
