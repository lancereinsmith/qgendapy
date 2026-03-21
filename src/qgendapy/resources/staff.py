from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.staff import (
    PayModifier,
    StaffMember,
    StaffProfile,
    StaffSkillset,
    StaffTag,
)
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class StaffResource(BaseResource):
    """Synchronous staff member endpoints."""

    def list(self, *, odata: OData | None = None) -> QGendaResponse[StaffMember]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        return self._get("/staffmember", params=params, model=StaffMember, odata=odata)

    def create(self, *, data: dict) -> QGendaResponse[StaffMember]:
        return self._post("/staffmember", json=data, model=StaffMember)

    def get(self, staff_key: str, *, odata: OData | None = None) -> QGendaResponse[StaffMember]:
        return self._get(f"/staffmember/{staff_key}", model=StaffMember, odata=odata)

    def update(self, staff_key: str, *, data: dict) -> QGendaResponse[StaffMember]:
        return self._put(f"/staffmember/{staff_key}", json=data, model=StaffMember)

    def locations(self, staff_key: str) -> QGendaResponse:
        return self._get(f"/staffmember/{staff_key}/location")

    def tags(self, staff_key: str) -> QGendaResponse[StaffTag]:
        return self._get(f"/staffmember/{staff_key}/tag", model=StaffTag)

    def add_tag(self, staff_key: str, *, data: dict) -> QGendaResponse[StaffTag]:
        return self._post(f"/staffmember/{staff_key}/tag", json=data, model=StaffTag)

    def update_location_tag(
        self, staff_key: str, location_key: str, *, data: dict
    ) -> QGendaResponse:
        return self._put(f"/staffmember/{staff_key}/location/{location_key}/tag", json=data)

    def skillsets(self, staff_key: str) -> QGendaResponse[StaffSkillset]:
        return self._get(f"/staffmember/{staff_key}/skillset", model=StaffSkillset)

    def update_skillset(
        self, staff_key: str, task_key: str, *, data: dict
    ) -> QGendaResponse[StaffSkillset]:
        return self._put(
            f"/staffmember/{staff_key}/skillset/{task_key}",
            json=data,
            model=StaffSkillset,
        )

    def delete_skillset(self, staff_key: str, task_key: str) -> QGendaResponse:
        return self._delete(f"/staffmember/{staff_key}/skillset/{task_key}")

    def profiles(self, staff_key: str) -> QGendaResponse[StaffProfile]:
        return self._get(f"/staffmember/{staff_key}/profile", model=StaffProfile)

    def update_profile(
        self, staff_key: str, profile_key: str, *, data: dict
    ) -> QGendaResponse[StaffProfile]:
        return self._put(
            f"/staffmember/{staff_key}/profile/{profile_key}",
            json=data,
            model=StaffProfile,
        )

    def pay_modifiers(self, staff_key: str) -> QGendaResponse[PayModifier]:
        return self._get(f"/staffmember/{staff_key}/payModifier", model=PayModifier)

    def create_pay_modifier(self, staff_key: str, *, data: dict) -> QGendaResponse[PayModifier]:
        return self._post(f"/staffmember/{staff_key}/payModifier", json=data, model=PayModifier)

    def update_pay_modifier(
        self, staff_key: str, pay_modifier_key: str, *, data: dict
    ) -> QGendaResponse[PayModifier]:
        return self._put(
            f"/staffmember/{staff_key}/payModifier/{pay_modifier_key}",
            json=data,
            model=PayModifier,
        )

    def delete_pay_modifier(self, staff_key: str, pay_modifier_key: str) -> QGendaResponse:
        return self._delete(f"/staffmember/{staff_key}/payModifier/{pay_modifier_key}")

    def badge_id(self, staff_key: str) -> QGendaResponse:
        return self._get(f"/staffmember/{staff_key}/badgeId")

    def request_limits(self, staff_key: str) -> QGendaResponse:
        return self._get(f"/staffmember/{staff_key}/requestlimit")

    def set_manager(self, staff_key: str, *, data: dict) -> QGendaResponse:
        return self._post(f"/staffmember/{staff_key}/manager", json=data)


class AsyncStaffResource(AsyncBaseResource):
    """Asynchronous staff member endpoints."""

    async def list(self, *, odata: OData | None = None) -> QGendaResponse[StaffMember]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        return await self._get("/staffmember", params=params, model=StaffMember, odata=odata)

    async def create(self, *, data: dict) -> QGendaResponse[StaffMember]:
        return await self._post("/staffmember", json=data, model=StaffMember)

    async def get(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[StaffMember]:
        return await self._get(f"/staffmember/{staff_key}", model=StaffMember, odata=odata)

    async def update(self, staff_key: str, *, data: dict) -> QGendaResponse[StaffMember]:
        return await self._put(f"/staffmember/{staff_key}", json=data, model=StaffMember)

    async def locations(self, staff_key: str) -> QGendaResponse:
        return await self._get(f"/staffmember/{staff_key}/location")

    async def tags(self, staff_key: str) -> QGendaResponse[StaffTag]:
        return await self._get(f"/staffmember/{staff_key}/tag", model=StaffTag)

    async def add_tag(self, staff_key: str, *, data: dict) -> QGendaResponse[StaffTag]:
        return await self._post(f"/staffmember/{staff_key}/tag", json=data, model=StaffTag)

    async def update_location_tag(
        self, staff_key: str, location_key: str, *, data: dict
    ) -> QGendaResponse:
        return await self._put(f"/staffmember/{staff_key}/location/{location_key}/tag", json=data)

    async def skillsets(self, staff_key: str) -> QGendaResponse[StaffSkillset]:
        return await self._get(f"/staffmember/{staff_key}/skillset", model=StaffSkillset)

    async def update_skillset(
        self, staff_key: str, task_key: str, *, data: dict
    ) -> QGendaResponse[StaffSkillset]:
        return await self._put(
            f"/staffmember/{staff_key}/skillset/{task_key}",
            json=data,
            model=StaffSkillset,
        )

    async def delete_skillset(self, staff_key: str, task_key: str) -> QGendaResponse:
        return await self._delete(f"/staffmember/{staff_key}/skillset/{task_key}")

    async def profiles(self, staff_key: str) -> QGendaResponse[StaffProfile]:
        return await self._get(f"/staffmember/{staff_key}/profile", model=StaffProfile)

    async def update_profile(
        self, staff_key: str, profile_key: str, *, data: dict
    ) -> QGendaResponse[StaffProfile]:
        return await self._put(
            f"/staffmember/{staff_key}/profile/{profile_key}",
            json=data,
            model=StaffProfile,
        )

    async def pay_modifiers(self, staff_key: str) -> QGendaResponse[PayModifier]:
        return await self._get(f"/staffmember/{staff_key}/payModifier", model=PayModifier)

    async def create_pay_modifier(
        self, staff_key: str, *, data: dict
    ) -> QGendaResponse[PayModifier]:
        return await self._post(
            f"/staffmember/{staff_key}/payModifier", json=data, model=PayModifier
        )

    async def update_pay_modifier(
        self, staff_key: str, pay_modifier_key: str, *, data: dict
    ) -> QGendaResponse[PayModifier]:
        return await self._put(
            f"/staffmember/{staff_key}/payModifier/{pay_modifier_key}",
            json=data,
            model=PayModifier,
        )

    async def delete_pay_modifier(self, staff_key: str, pay_modifier_key: str) -> QGendaResponse:
        return await self._delete(f"/staffmember/{staff_key}/payModifier/{pay_modifier_key}")

    async def badge_id(self, staff_key: str) -> QGendaResponse:
        return await self._get(f"/staffmember/{staff_key}/badgeId")

    async def request_limits(self, staff_key: str) -> QGendaResponse:
        return await self._get(f"/staffmember/{staff_key}/requestlimit")

    async def set_manager(self, staff_key: str, *, data: dict) -> QGendaResponse:
        return await self._post(f"/staffmember/{staff_key}/manager", json=data)
