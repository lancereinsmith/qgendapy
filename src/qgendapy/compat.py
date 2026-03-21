"""Drop-in replacement for the legacy ``python-qgenda`` library.

Usage::

    from qgendapy.compat import QGendaClient

    client = QGendaClient(username="user@example.com", password="secret",
                          company_key="abc123")
    client.authenticate()  # no-op, modern client auto-authenticates
    resp = client.get_schedule(start_date="2024-01-01")
    data = resp.json()
"""

from __future__ import annotations

import json as _json
from typing import TYPE_CHECKING

from qgendapy.client import QGendaClient as _ModernClient
from qgendapy.odata import OData

if TYPE_CHECKING:
    from qgendapy.response import QGendaResponse

_DEFAULT_API_URL = "https://api.qgenda.com"
_DEFAULT_API_VERSION = "v2"


class _CompatResponse:
    """Mimics ``requests.Response`` for legacy code."""

    def __init__(self, qgenda_response: QGendaResponse) -> None:
        self.status_code: int = qgenda_response.status_code
        self.headers: dict[str, str] = qgenda_response.headers
        self._data = qgenda_response.data

    def json(self) -> list | dict:
        return self._data

    @property
    def text(self) -> str:
        return _json.dumps(self._data)


def _build_odata(odata_kwargs: dict | None) -> OData | None:
    """Convert legacy odata_kwargs dict to an OData builder, or None."""
    if not odata_kwargs:
        return None
    return OData.from_kwargs(odata_kwargs)


class QGendaClient:
    """Legacy-compatible client matching ``python-qgenda``'s QGendaClient API."""

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        company_key: str | None = None,
        api_url: str | None = None,
        api_version: str | None = None,
        headers: dict | None = None,
        raise_errors: bool = True,
        use_caching: bool = False,
        leader: bool = True,
    ) -> None:
        url = api_url or _DEFAULT_API_URL
        version = api_version or _DEFAULT_API_VERSION
        base_url = f"{url.rstrip('/')}/{version}"

        self._client = _ModernClient(
            email=username,
            password=password,
            company_key=company_key,
            base_url=base_url,
        )
        self._raise_errors = raise_errors

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self) -> None:
        """No-op -- modern client auto-authenticates on first request."""

    # ------------------------------------------------------------------
    # Schedule
    # ------------------------------------------------------------------

    def get_schedule(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        odata_kwargs: dict | None = None,
        headers: dict | None = None,
    ) -> _CompatResponse:
        odata = _build_odata(odata_kwargs)
        if not start_date:
            raise ValueError("start_date is required for get_schedule")
        resp = self._client.schedule.list(
            start_date=start_date,
            end_date=end_date,
            odata=odata,
        )
        return _CompatResponse(resp)

    # ------------------------------------------------------------------
    # Staff
    # ------------------------------------------------------------------

    def get_staff(
        self,
        odata_kwargs: dict | None = None,
        headers: dict | None = None,
    ) -> _CompatResponse:
        odata = _build_odata(odata_kwargs)
        resp = self._client.staff.list(odata=odata)
        return _CompatResponse(resp)

    # ------------------------------------------------------------------
    # Facility
    # ------------------------------------------------------------------

    def get_facility(
        self,
        odata_kwargs: dict | None = None,
        headers: dict | None = None,
    ) -> _CompatResponse:
        odata = _build_odata(odata_kwargs)
        resp = self._client.facility.list(odata=odata)
        return _CompatResponse(resp)

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    def get_organization(
        self,
        odata_kwargs: dict | None = None,
        headers: dict | None = None,
        organization_key: str | None = None,
    ) -> _CompatResponse:
        odata = _build_odata(odata_kwargs)
        resp = self._client.organization.list(odata=odata)
        return _CompatResponse(resp)

    # ------------------------------------------------------------------
    # Task
    # ------------------------------------------------------------------

    def get_task(
        self,
        odata_kwargs: dict | None = None,
        headers: dict | None = None,
    ) -> _CompatResponse:
        odata = _build_odata(odata_kwargs)
        resp = self._client.task.list(odata=odata)
        return _CompatResponse(resp)

    # ------------------------------------------------------------------
    # Time Event
    # ------------------------------------------------------------------

    def get_timeevent(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        odata_kwargs: dict | None = None,
        headers: dict | None = None,
    ) -> _CompatResponse:
        odata = _build_odata(odata_kwargs)
        if not start_date:
            raise ValueError("start_date is required for get_timeevent")
        resp = self._client.time_event.list(
            start_date=start_date,
            end_date=end_date,
            odata=odata,
        )
        return _CompatResponse(resp)

    # ------------------------------------------------------------------
    # Daily Case
    # ------------------------------------------------------------------

    def get_dailycase(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        odata_kwargs: dict | None = None,
        headers: dict | None = None,
    ) -> _CompatResponse:
        odata = _build_odata(odata_kwargs)
        if not start_date:
            raise ValueError("start_date is required for get_dailycase")
        resp = self._client.daily_case.list(
            start_date=start_date,
            end_date=end_date,
            odata=odata,
        )
        return _CompatResponse(resp)
