from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from qgendapy.exceptions import QGendaError
from qgendapy.models.schedule import AuditLogEntry, OpenShift, Rotation, ScheduleEntry
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse

_MAX_DAYS = 100


def _date_chunks(start: str, end: str) -> list[tuple[str, str]]:
    """Split a date range into chunks of at most _MAX_DAYS days."""
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    if (e - s).days <= _MAX_DAYS:
        return [(start, end)]
    chunks: list[tuple[str, str]] = []
    while s <= e:
        chunk_end = min(s + timedelta(days=_MAX_DAYS), e)
        chunks.append((s.isoformat(), chunk_end.isoformat()))
        s = chunk_end + timedelta(days=1)
    return chunks


class ScheduleResource(BaseResource):
    """Synchronous schedule endpoints."""

    def list(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        includes: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[ScheduleEntry]:
        if end_date and _date_chunks(start_date, end_date) != [(start_date, end_date)]:
            return self._chunked_list(
                start_date=start_date, end_date=end_date, includes=includes, odata=odata
            )
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        if includes:
            params["includes"] = includes
        return self._get("/schedule", params=params, model=ScheduleEntry, odata=odata)

    def _chunked_list(
        self,
        *,
        start_date: str,
        end_date: str,
        includes: str | None,
        odata: OData | None,
    ) -> QGendaResponse[ScheduleEntry]:
        chunks = _date_chunks(start_date, end_date)
        combined: QGendaResponse[ScheduleEntry] | None = None
        for chunk_start, chunk_end in chunks:
            resp = self.list(
                start_date=chunk_start, end_date=chunk_end, includes=includes, odata=odata
            )
            if combined is None:
                combined = resp
            else:
                if isinstance(combined.data, list) and isinstance(resp.data, list):
                    combined.data.extend(resp.data)
                combined.items.extend(resp.items)
        if combined is None:
            raise QGendaError("No responses received from chunked schedule request")
        return combined

    def audit_log(
        self,
        *,
        schedule_start_date: str | None = None,
        schedule_end_date: str | None = None,
        since_modified_timestamp: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[AuditLogEntry]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        if schedule_start_date:
            params["scheduleStartDate"] = schedule_start_date
        if schedule_end_date:
            params["scheduleEndDate"] = schedule_end_date
        if since_modified_timestamp:
            params["sinceModifiedTimestamp"] = since_modified_timestamp
        return self._get("/schedule/auditLog", params=params, model=AuditLogEntry, odata=odata)

    def open_shifts(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        includes: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[OpenShift]:
        if end_date and _date_chunks(start_date, end_date) != [(start_date, end_date)]:
            return self._chunked_open_shifts(
                start_date=start_date, end_date=end_date, includes=includes, odata=odata
            )
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        if includes:
            params["includes"] = includes
        return self._get("/schedule/openshifts", params=params, model=OpenShift, odata=odata)

    def _chunked_open_shifts(
        self,
        *,
        start_date: str,
        end_date: str,
        includes: str | None,
        odata: OData | None,
    ) -> QGendaResponse[OpenShift]:
        chunks = _date_chunks(start_date, end_date)
        combined: QGendaResponse[OpenShift] | None = None
        for chunk_start, chunk_end in chunks:
            resp = self.open_shifts(
                start_date=chunk_start, end_date=chunk_end, includes=includes, odata=odata
            )
            if combined is None:
                combined = resp
            else:
                if isinstance(combined.data, list) and isinstance(resp.data, list):
                    combined.data.extend(resp.data)
                combined.items.extend(resp.items)
        if combined is None:
            raise QGendaError("No responses received from chunked schedule request")
        return combined

    def rotations(
        self,
        *,
        range_start_date: str | None = None,
        range_end_date: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[Rotation]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        if range_start_date:
            params["rangeStartDate"] = range_start_date
        if range_end_date:
            params["rangeEndDate"] = range_end_date
        return self._get("/schedule/rotations", params=params, model=Rotation, odata=odata)


class AsyncScheduleResource(AsyncBaseResource):
    """Asynchronous schedule endpoints."""

    async def list(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        includes: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[ScheduleEntry]:
        if end_date and _date_chunks(start_date, end_date) != [(start_date, end_date)]:
            return await self._chunked_list(
                start_date=start_date, end_date=end_date, includes=includes, odata=odata
            )
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        if includes:
            params["includes"] = includes
        return await self._get("/schedule", params=params, model=ScheduleEntry, odata=odata)

    async def _chunked_list(
        self,
        *,
        start_date: str,
        end_date: str,
        includes: str | None,
        odata: OData | None,
    ) -> QGendaResponse[ScheduleEntry]:
        chunks = _date_chunks(start_date, end_date)
        combined: QGendaResponse[ScheduleEntry] | None = None
        for chunk_start, chunk_end in chunks:
            resp = await self.list(
                start_date=chunk_start, end_date=chunk_end, includes=includes, odata=odata
            )
            if combined is None:
                combined = resp
            else:
                if isinstance(combined.data, list) and isinstance(resp.data, list):
                    combined.data.extend(resp.data)
                combined.items.extend(resp.items)
        if combined is None:
            raise QGendaError("No responses received from chunked schedule request")
        return combined

    async def audit_log(
        self,
        *,
        schedule_start_date: str | None = None,
        schedule_end_date: str | None = None,
        since_modified_timestamp: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[AuditLogEntry]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        if schedule_start_date:
            params["scheduleStartDate"] = schedule_start_date
        if schedule_end_date:
            params["scheduleEndDate"] = schedule_end_date
        if since_modified_timestamp:
            params["sinceModifiedTimestamp"] = since_modified_timestamp
        return await self._get(
            "/schedule/auditLog", params=params, model=AuditLogEntry, odata=odata
        )

    async def open_shifts(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        includes: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[OpenShift]:
        if end_date and _date_chunks(start_date, end_date) != [(start_date, end_date)]:
            return await self._chunked_open_shifts(
                start_date=start_date, end_date=end_date, includes=includes, odata=odata
            )
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        if includes:
            params["includes"] = includes
        return await self._get("/schedule/openshifts", params=params, model=OpenShift, odata=odata)

    async def _chunked_open_shifts(
        self,
        *,
        start_date: str,
        end_date: str,
        includes: str | None,
        odata: OData | None,
    ) -> QGendaResponse[OpenShift]:
        chunks = _date_chunks(start_date, end_date)
        combined: QGendaResponse[OpenShift] | None = None
        for chunk_start, chunk_end in chunks:
            resp = await self.open_shifts(
                start_date=chunk_start, end_date=chunk_end, includes=includes, odata=odata
            )
            if combined is None:
                combined = resp
            else:
                if isinstance(combined.data, list) and isinstance(resp.data, list):
                    combined.data.extend(resp.data)
                combined.items.extend(resp.items)
        if combined is None:
            raise QGendaError("No responses received from chunked schedule request")
        return combined

    async def rotations(
        self,
        *,
        range_start_date: str | None = None,
        range_end_date: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[Rotation]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        if range_start_date:
            params["rangeStartDate"] = range_start_date
        if range_end_date:
            params["rangeEndDate"] = range_end_date
        return await self._get("/schedule/rotations", params=params, model=Rotation, odata=odata)
