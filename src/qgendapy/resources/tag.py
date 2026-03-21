from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.common import Tag
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class TagResource(BaseResource):
    """Synchronous tag endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[Tag]:
        return self._get("/tags", model=Tag, odata=odata)


class AsyncTagResource(AsyncBaseResource):
    """Asynchronous tag endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[Tag]:
        return await self._get("/tags", model=Tag, odata=odata)
