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
        """List all tags in the company.

        **Requires an admin-scoped QGenda account.** Service accounts
        provisioned only for schedule reads will get a 401 with the message
        ``User does not have admin permission for any company``. Catch
        :class:`qgendapy.exceptions.APIError` if you call this from code
        that may run under non-admin credentials.
        """
        return self._get("/tags", model=Tag, odata=odata)


class AsyncTagResource(AsyncBaseResource):
    """Asynchronous tag endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[Tag]:
        """Async version of :meth:`TagResource.list` — requires admin scope."""
        return await self._get("/tags", model=Tag, odata=odata)
