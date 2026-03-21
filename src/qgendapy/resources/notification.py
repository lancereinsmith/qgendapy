from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class NotificationResource(BaseResource):
    """Synchronous notification list endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse:
        return self._get("/notificationlist", odata=odata)

    def create(self, *, data: dict) -> QGendaResponse:
        return self._post("/notificationlist", json=data)

    def get(self, notification_list_key: str, *, odata: OData | None = None) -> QGendaResponse:
        return self._get(f"/notificationlist/{notification_list_key}", odata=odata)

    def update(self, notification_list_key: str, *, data: dict) -> QGendaResponse:
        return self._put(f"/notificationlist/{notification_list_key}", json=data)

    def delete(self, notification_list_key: str) -> QGendaResponse:
        return self._delete(f"/notificationlist/{notification_list_key}")

    def contacts(self, notification_list_key: str) -> QGendaResponse:
        return self._get(f"/notificationlist/{notification_list_key}/contact")

    def add_contact(self, notification_list_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/notificationlist/{notification_list_key}/contact", json=data)

    def update_contact(self, notification_list_key: str, *, data: dict) -> QGendaResponse:
        return self._put(f"/notificationlist/{notification_list_key}/contact", json=data)

    def remove_contact(self, notification_list_key: str, *, data: dict) -> QGendaResponse:
        return self._delete(f"/notificationlist/{notification_list_key}/contact", json=data)


class AsyncNotificationResource(AsyncBaseResource):
    """Asynchronous notification list endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse:
        return await self._get("/notificationlist", odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse:
        return await self._post("/notificationlist", json=data)

    async def get(
        self, notification_list_key: str, *, odata: OData | None = None
    ) -> QGendaResponse:
        return await self._get(f"/notificationlist/{notification_list_key}", odata=odata)

    async def update(self, notification_list_key: str, *, data: dict) -> QGendaResponse:
        return await self._put(f"/notificationlist/{notification_list_key}", json=data)

    async def delete(self, notification_list_key: str) -> QGendaResponse:
        return await self._delete(f"/notificationlist/{notification_list_key}")

    async def contacts(self, notification_list_key: str) -> QGendaResponse:
        return await self._get(f"/notificationlist/{notification_list_key}/contact")

    async def add_contact(self, notification_list_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/notificationlist/{notification_list_key}/contact", json=data)

    async def update_contact(self, notification_list_key: str, *, data: dict) -> QGendaResponse:
        return await self._put(f"/notificationlist/{notification_list_key}/contact", json=data)

    async def remove_contact(self, notification_list_key: str, *, data: dict) -> QGendaResponse:
        return await self._delete(f"/notificationlist/{notification_list_key}/contact", json=data)
