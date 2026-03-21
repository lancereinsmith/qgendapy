from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.request import ApprovedRequest, Request
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class RequestResource(BaseResource):
    """Synchronous request endpoints."""

    def list(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        include_removed: bool | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[Request]:
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        if include_removed is not None:
            params["includeRemoved"] = str(include_removed).lower()
        return self._get("/request", params=params, model=Request, odata=odata)

    def approved(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[ApprovedRequest]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        return self._get("/request/approved", params=params, model=ApprovedRequest, odata=odata)


class AsyncRequestResource(AsyncBaseResource):
    """Asynchronous request endpoints."""

    async def list(
        self,
        *,
        start_date: str,
        end_date: str | None = None,
        include_removed: bool | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[Request]:
        params: dict[str, str] = {
            "startDate": start_date,
            "companyKey": self._client.company_key,
        }
        if end_date:
            params["endDate"] = end_date
        if include_removed is not None:
            params["includeRemoved"] = str(include_removed).lower()
        return await self._get("/request", params=params, model=Request, odata=odata)

    async def approved(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[ApprovedRequest]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        return await self._get(
            "/request/approved", params=params, model=ApprovedRequest, odata=odata
        )
