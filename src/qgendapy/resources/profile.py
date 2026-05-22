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
        """List all profiles in the company.

        **Requires an admin-scoped QGenda account.** Service accounts
        provisioned only for schedule reads will get a 401 with the message
        ``No valid profile exists for user in company provided``. Catch
        :class:`qgendapy.exceptions.APIError` if you call this from code
        that may run under non-admin credentials.
        """
        return self._get("/profile", model=Profile, odata=odata)


class AsyncProfileResource(AsyncBaseResource):
    """Asynchronous profile endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[Profile]:
        """Async version of :meth:`ProfileResource.list` — requires admin scope."""
        return await self._get("/profile", model=Profile, odata=odata)
