from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from qgendapy.models.staff import (
    PayModifier,
    StaffMember,
    StaffProfile,
    StaffSkillset,
    StaffTag,
)
from qgendapy.odata import OData, escape_literal, merge_expand
from qgendapy.resources._base import AsyncBaseResource, BaseResource
from qgendapy.response import QGendaResponse

if TYPE_CHECKING:
    pass


def _extract_nested(
    list_data: list | dict,
    nav_property: str,
) -> list[dict]:
    """Pull a navigation-property collection out of a /staffmember list response."""
    items: list[dict] = []
    members: list = list_data if isinstance(list_data, list) else [list_data]
    for member in members:
        if not isinstance(member, dict):
            continue
        nested = member.get(nav_property)
        if isinstance(nested, list):
            items.extend(d for d in nested if isinstance(d, dict))
        elif isinstance(nested, dict):
            items.append(nested)
    return items


class StaffResource(BaseResource):
    """Synchronous staff member endpoints."""

    def list(
        self,
        *,
        odata: OData | None = None,
        expand: str | Sequence[str] | None = None,
        includes: str | None = None,
    ) -> QGendaResponse[StaffMember]:
        """List staff members.

        ``expand`` is a convenience shortcut for ``OData().expand(...)`` —
        pass a string (``expand="Tags"``) or a list of nav properties to
        request expanded entities. Valid OData v4 nav names on
        ``StaffMemberDetailDto`` include ``Tags``, ``Skillset`` (singular),
        and ``Profiles``.

        ``includes`` is QGenda's own related-entity selector (separate from
        OData ``$expand``). For schedule-style endpoints it returns rich
        nested data even under non-admin scope; on ``/staffmember`` its
        behavior should be verified per-deployment.
        """
        params: dict[str, str] = {"companyKey": self._client.company_key}
        if includes:
            params["includes"] = includes
        return self._get(
            "/staffmember",
            params=params,
            model=StaffMember,
            odata=merge_expand(expand, odata),
        )

    def create(self, *, data: dict) -> QGendaResponse[StaffMember]:
        return self._post("/staffmember", json=data, model=StaffMember)

    def get(
        self,
        staff_key: str,
        *,
        odata: OData | None = None,
        expand: str | Sequence[str] | None = None,
        includes: str | None = None,
    ) -> QGendaResponse[StaffMember]:
        params: dict[str, str] = {}
        if includes:
            params["includes"] = includes
        return self._get(
            f"/staffmember/{staff_key}",
            params=params or None,
            model=StaffMember,
            odata=merge_expand(expand, odata),
        )

    def update(self, staff_key: str, *, data: dict) -> QGendaResponse[StaffMember]:
        return self._put(f"/staffmember/{staff_key}", json=data, model=StaffMember)

    def locations(self, staff_key: str) -> QGendaResponse:
        return self._get(f"/staffmember/{staff_key}/location")

    def tags(self, staff_key: str) -> QGendaResponse[StaffTag]:
        """Return tags for a single staff member.

        QGenda's API does not expose ``GET /staffmember/{key}/tag`` (it
        returns 405). This method instead issues
        ``GET /staffmember?$filter=StaffKey eq '<key>'&$expand=Tags`` and
        unwraps the ``Tags`` navigation collection.

        **Returns an empty list under non-admin scope.** The ``Tags``
        navigation property exists on QGenda's DTO but only populates for
        admin-scoped service accounts. If you need tag/profile catalogs,
        provision the API user with admin scope and call
        ``client.tag.list()``.
        """
        params: dict[str, str] = {"companyKey": self._client.company_key}
        odata = OData().filter(f"StaffKey eq '{escape_literal(staff_key)}'").expand("Tags")
        raw = self._get("/staffmember", params=params, odata=odata)
        tag_dicts = _extract_nested(raw.data, "Tags")
        return QGendaResponse(
            data=tag_dicts,
            status_code=raw.status_code,
            headers=raw.headers,
            items=[StaffTag.from_dict(d) for d in tag_dicts],
        )

    def add_tag(self, staff_key: str, *, data: dict) -> QGendaResponse[StaffTag]:
        return self._post(f"/staffmember/{staff_key}/tag", json=data, model=StaffTag)

    def update_location_tag(
        self, staff_key: str, location_key: str, *, data: dict
    ) -> QGendaResponse:
        return self._put(f"/staffmember/{staff_key}/location/{location_key}/tag", json=data)

    def skillsets(self, staff_key: str) -> QGendaResponse[StaffSkillset]:
        """Return skillsets for a single staff member.

        QGenda's API does not expose ``GET /staffmember/{key}/skillset`` (it
        returns 405). This method instead issues
        ``GET /staffmember?$filter=StaffKey eq '<key>'&$expand=Skillset`` —
        note the singular ``Skillset`` nav property — and unwraps the
        navigation collection.

        **Returns an empty list under non-admin scope.** Like ``Tags``, the
        ``Skillset`` navigation populates only for admin-scoped accounts.
        """
        params: dict[str, str] = {"companyKey": self._client.company_key}
        odata = OData().filter(f"StaffKey eq '{escape_literal(staff_key)}'").expand("Skillset")
        raw = self._get("/staffmember", params=params, odata=odata)
        skillset_dicts = _extract_nested(raw.data, "Skillset")
        return QGendaResponse(
            data=skillset_dicts,
            status_code=raw.status_code,
            headers=raw.headers,
            items=[StaffSkillset.from_dict(d) for d in skillset_dicts],
        )

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

    async def list(
        self,
        *,
        odata: OData | None = None,
        expand: str | Sequence[str] | None = None,
        includes: str | None = None,
    ) -> QGendaResponse[StaffMember]:
        params: dict[str, str] = {"companyKey": self._client.company_key}
        if includes:
            params["includes"] = includes
        return await self._get(
            "/staffmember",
            params=params,
            model=StaffMember,
            odata=merge_expand(expand, odata),
        )

    async def create(self, *, data: dict) -> QGendaResponse[StaffMember]:
        return await self._post("/staffmember", json=data, model=StaffMember)

    async def get(
        self,
        staff_key: str,
        *,
        odata: OData | None = None,
        expand: str | Sequence[str] | None = None,
        includes: str | None = None,
    ) -> QGendaResponse[StaffMember]:
        params: dict[str, str] = {}
        if includes:
            params["includes"] = includes
        return await self._get(
            f"/staffmember/{staff_key}",
            params=params or None,
            model=StaffMember,
            odata=merge_expand(expand, odata),
        )

    async def update(self, staff_key: str, *, data: dict) -> QGendaResponse[StaffMember]:
        return await self._put(f"/staffmember/{staff_key}", json=data, model=StaffMember)

    async def locations(self, staff_key: str) -> QGendaResponse:
        return await self._get(f"/staffmember/{staff_key}/location")

    async def tags(self, staff_key: str) -> QGendaResponse[StaffTag]:
        """Async version of :meth:`StaffResource.tags`."""
        params: dict[str, str] = {"companyKey": self._client.company_key}
        odata = OData().filter(f"StaffKey eq '{escape_literal(staff_key)}'").expand("Tags")
        raw = await self._get("/staffmember", params=params, odata=odata)
        tag_dicts = _extract_nested(raw.data, "Tags")
        return QGendaResponse(
            data=tag_dicts,
            status_code=raw.status_code,
            headers=raw.headers,
            items=[StaffTag.from_dict(d) for d in tag_dicts],
        )

    async def add_tag(self, staff_key: str, *, data: dict) -> QGendaResponse[StaffTag]:
        return await self._post(f"/staffmember/{staff_key}/tag", json=data, model=StaffTag)

    async def update_location_tag(
        self, staff_key: str, location_key: str, *, data: dict
    ) -> QGendaResponse:
        return await self._put(f"/staffmember/{staff_key}/location/{location_key}/tag", json=data)

    async def skillsets(self, staff_key: str) -> QGendaResponse[StaffSkillset]:
        """Async version of :meth:`StaffResource.skillsets`."""
        params: dict[str, str] = {"companyKey": self._client.company_key}
        odata = OData().filter(f"StaffKey eq '{escape_literal(staff_key)}'").expand("Skillset")
        raw = await self._get("/staffmember", params=params, odata=odata)
        skillset_dicts = _extract_nested(raw.data, "Skillset")
        return QGendaResponse(
            data=skillset_dicts,
            status_code=raw.status_code,
            headers=raw.headers,
            items=[StaffSkillset.from_dict(d) for d in skillset_dicts],
        )

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
