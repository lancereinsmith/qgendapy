from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.daily import DailyCase
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class DailyCaseResource(BaseResource):
    """Synchronous daily case endpoints."""

    def list(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[DailyCase]:
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        return self._get("/dailycase", params=params, model=DailyCase, odata=odata)

    def create(self, *, data: dict) -> QGendaResponse[DailyCase]:
        return self._post("/dailycase", json=data, model=DailyCase)

    def update(self, daily_case_key: str, *, data: dict) -> QGendaResponse[DailyCase]:
        return self._put(f"/dailycase/{daily_case_key}", json=data, model=DailyCase)

    def delete(self, daily_case_key: str) -> QGendaResponse:
        return self._delete(f"/dailycase/{daily_case_key}")


class AsyncDailyCaseResource(AsyncBaseResource):
    """Asynchronous daily case endpoints."""

    async def list(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[DailyCase]:
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        return await self._get("/dailycase", params=params, model=DailyCase, odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse[DailyCase]:
        return await self._post("/dailycase", json=data, model=DailyCase)

    async def update(self, daily_case_key: str, *, data: dict) -> QGendaResponse[DailyCase]:
        return await self._put(f"/dailycase/{daily_case_key}", json=data, model=DailyCase)

    async def delete(self, daily_case_key: str) -> QGendaResponse:
        return await self._delete(f"/dailycase/{daily_case_key}")
