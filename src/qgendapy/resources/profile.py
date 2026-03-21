from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.common import Profile
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class ProfileResource(BaseResource):
    """Synchronous profile endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[Profile]:
        return self._get("/profile", model=Profile, odata=odata)


class AsyncProfileResource(AsyncBaseResource):
    """Asynchronous profile endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[Profile]:
        return await self._get("/profile", model=Profile, odata=odata)
