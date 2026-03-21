from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class CreditAllocationResource(BaseResource):
    """Synchronous credit allocation endpoints."""

    def quotas(self, *, odata: OData | None = None) -> QGendaResponse[dict]:
        # QGenda API uses PascalCase for this endpoint
        return self._get("/CreditAllocation/Quota", odata=odata)

    def update_quota(
        self, credit_allocation_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse[dict]:
        return self._put(
            f"/creditallocation/{credit_allocation_key}/quota/{staff_key}",
            json=data,
        )


class AsyncCreditAllocationResource(AsyncBaseResource):
    """Asynchronous credit allocation endpoints."""

    async def quotas(self, *, odata: OData | None = None) -> QGendaResponse[dict]:
        # QGenda API uses PascalCase for this endpoint
        return await self._get("/CreditAllocation/Quota", odata=odata)

    async def update_quota(
        self, credit_allocation_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse[dict]:
        return await self._put(
            f"/creditallocation/{credit_allocation_key}/quota/{staff_key}",
            json=data,
        )
