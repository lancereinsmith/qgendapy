from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.pay import PayCode, PayPeriodAmount, PayRate
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class PayCodeResource(BaseResource):
    """Synchronous pay code endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[PayCode]:
        return self._get("/PayCode", model=PayCode, odata=odata)


class AsyncPayCodeResource(AsyncBaseResource):
    """Asynchronous pay code endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[PayCode]:
        return await self._get("/PayCode", model=PayCode, odata=odata)


class PayRateResource(BaseResource):
    """Synchronous pay rate endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[PayRate]:
        return self._get("/payrate", model=PayRate, odata=odata)

    def create(self, *, data: dict) -> QGendaResponse[PayRate]:
        return self._post("/payrate", json=data, model=PayRate)

    def update(self, pay_rate_key: str, *, data: dict) -> QGendaResponse[PayRate]:
        return self._put(f"/payrate/{pay_rate_key}", json=data, model=PayRate)

    def delete(self, pay_rate_key: str) -> QGendaResponse:
        return self._delete(f"/payrate/{pay_rate_key}")


class AsyncPayRateResource(AsyncBaseResource):
    """Asynchronous pay rate endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[PayRate]:
        return await self._get("/payrate", model=PayRate, odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse[PayRate]:
        return await self._post("/payrate", json=data, model=PayRate)

    async def update(self, pay_rate_key: str, *, data: dict) -> QGendaResponse[PayRate]:
        return await self._put(f"/payrate/{pay_rate_key}", json=data, model=PayRate)

    async def delete(self, pay_rate_key: str) -> QGendaResponse:
        return await self._delete(f"/payrate/{pay_rate_key}")


class PayPoolResource(BaseResource):
    """Synchronous pay pool endpoints."""

    def period_amounts(
        self, pay_pool_template_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[PayPeriodAmount]:
        return self._get(
            f"/PayPoolTemplate/{pay_pool_template_key}/PayPeriodAmount",
            model=PayPeriodAmount,
            odata=odata,
        )


class AsyncPayPoolResource(AsyncBaseResource):
    """Asynchronous pay pool endpoints."""

    async def period_amounts(
        self, pay_pool_template_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[PayPeriodAmount]:
        return await self._get(
            f"/PayPoolTemplate/{pay_pool_template_key}/PayPeriodAmount",
            model=PayPeriodAmount,
            odata=odata,
        )
