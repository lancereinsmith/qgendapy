from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.time_event import TimeEvent
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class TimeEventResource(BaseResource):
    """Synchronous time event endpoints."""

    def list(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[TimeEvent]:
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        return self._get("/timeevent", params=params, model=TimeEvent, odata=odata)

    def create(self, *, data: dict) -> QGendaResponse[TimeEvent]:
        return self._post("/timeevent", json=data, model=TimeEvent)

    def update(self, time_event_key: str, *, data: dict) -> QGendaResponse[TimeEvent]:
        return self._put(f"/timeevent/{time_event_key}", json=data, model=TimeEvent)

    def delete(self, time_event_key: str) -> QGendaResponse:
        return self._delete(f"/timeevent/{time_event_key}")


class AsyncTimeEventResource(AsyncBaseResource):
    """Asynchronous time event endpoints."""

    async def list(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[TimeEvent]:
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        return await self._get("/timeevent", params=params, model=TimeEvent, odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse[TimeEvent]:
        return await self._post("/timeevent", json=data, model=TimeEvent)

    async def update(self, time_event_key: str, *, data: dict) -> QGendaResponse[TimeEvent]:
        return await self._put(f"/timeevent/{time_event_key}", json=data, model=TimeEvent)

    async def delete(self, time_event_key: str) -> QGendaResponse:
        return await self._delete(f"/timeevent/{time_event_key}")
