"""Tests for async resource variants.

Covers all HTTP method paths (_get, _post, _put, _delete) through
AsyncBaseResource, using schedule (GET), staff (CRUD), and daily_case (DELETE)
as representative resources.
"""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qgendapy.models.schedule import ScheduleEntry
from qgendapy.models.staff import StaffMember, StaffTag
from qgendapy.odata import OData
from qgendapy.resources.daily_case import AsyncDailyCaseResource
from qgendapy.resources.schedule import AsyncScheduleResource
from qgendapy.resources.staff import AsyncStaffResource


def _mock_async_client(response_data, status_code=200, method="GET"):
    client = MagicMock()
    client.company_key = "test-key"
    resp = httpx.Response(
        status_code,
        json=response_data,
        request=httpx.Request(method, "http://test"),
    )
    client._transport.request = AsyncMock(return_value=resp)
    return client


# ---------- AsyncScheduleResource (GET path) ----------


class TestAsyncScheduleList:
    @pytest.mark.asyncio
    async def test_returns_schedule_entries(self):
        data = [{"ScheduleKey": "sk1", "StaffFName": "John", "TaskName": "Reading"}]
        client = _mock_async_client(data)
        resource = AsyncScheduleResource(client)
        resp = await resource.list(start_date="2024-01-01")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], ScheduleEntry)
        assert resp.items[0].schedule_key == "sk1"

    @pytest.mark.asyncio
    async def test_passes_required_params(self):
        client = _mock_async_client([])
        resource = AsyncScheduleResource(client)
        await resource.list(start_date="2024-01-01")

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["startDate"] == "2024-01-01"
        assert params["companyKey"] == "test-key"

    @pytest.mark.asyncio
    async def test_passes_optional_params(self):
        client = _mock_async_client([])
        resource = AsyncScheduleResource(client)
        await resource.list(start_date="2024-01-01", end_date="2024-01-31", includes="Task")

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["endDate"] == "2024-01-31"
        assert params["includes"] == "Task"

    @pytest.mark.asyncio
    async def test_odata_merged_into_params(self):
        client = _mock_async_client([])
        resource = AsyncScheduleResource(client)
        odata = OData().select("ScheduleKey").filter("IsPublished eq true")
        await resource.list(start_date="2024-01-01", odata=odata)

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert "$select" in params
        assert "$filter" in params


class TestAsyncScheduleAuditLog:
    @pytest.mark.asyncio
    async def test_hits_correct_path(self):
        client = _mock_async_client([])
        resource = AsyncScheduleResource(client)
        await resource.audit_log()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/schedule/auditLog"


class TestAsyncScheduleOpenShifts:
    @pytest.mark.asyncio
    async def test_hits_correct_path(self):
        client = _mock_async_client([])
        resource = AsyncScheduleResource(client)
        await resource.open_shifts(start_date="2024-01-01")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/schedule/openshifts"


class TestAsyncScheduleRotations:
    @pytest.mark.asyncio
    async def test_hits_correct_path(self):
        client = _mock_async_client([])
        resource = AsyncScheduleResource(client)
        await resource.rotations()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/schedule/rotations"


# ---------- AsyncStaffResource (POST / PUT / GET path) ----------


class TestAsyncStaffList:
    @pytest.mark.asyncio
    async def test_returns_staff_members(self):
        data = [{"StaffKey": "s1", "FirstName": "Jane", "LastName": "Doe"}]
        client = _mock_async_client(data)
        resource = AsyncStaffResource(client)
        resp = await resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], StaffMember)
        assert resp.items[0].first_name == "Jane"


class TestAsyncStaffCreate:
    @pytest.mark.asyncio
    async def test_posts_to_correct_path(self):
        client = _mock_async_client({"StaffKey": "new"}, method="POST")
        resource = AsyncStaffResource(client)
        await resource.create(data={"FirstName": "New"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/staffmember"
        assert call_args.kwargs["json"] == {"FirstName": "New"}


class TestAsyncStaffUpdate:
    @pytest.mark.asyncio
    async def test_puts_to_correct_path(self):
        client = _mock_async_client({"StaffKey": "s1"}, method="PUT")
        resource = AsyncStaffResource(client)
        await resource.update("s1", data={"FirstName": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/staffmember/s1"


class TestAsyncStaffTags:
    @pytest.mark.asyncio
    async def test_returns_staff_tags(self):
        data = [{"TagKey": "t1", "TagName": "Senior"}]
        client = _mock_async_client(data)
        resource = AsyncStaffResource(client)
        resp = await resource.tags("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], StaffTag)

    @pytest.mark.asyncio
    async def test_add_tag_posts(self):
        client = _mock_async_client({"TagKey": "t1"}, method="POST")
        resource = AsyncStaffResource(client)
        await resource.add_tag("s1", data={"TagName": "New"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/staffmember/s1/tag"


# ---------- AsyncDailyCaseResource (DELETE path) ----------


class TestAsyncDailyCaseDelete:
    @pytest.mark.asyncio
    async def test_deletes_to_correct_path(self):
        client = _mock_async_client(None, method="DELETE")
        # DELETE returns empty body, mock accordingly
        resp = httpx.Response(
            204,
            content=b"",
            request=httpx.Request("DELETE", "http://test"),
        )
        client._transport.request = AsyncMock(return_value=resp)
        resource = AsyncDailyCaseResource(client)
        await resource.delete("dc1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/dailycase/dc1"
