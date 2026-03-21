from unittest.mock import MagicMock

import httpx

from qgendapy.models.staff import PayModifier, StaffMember, StaffSkillset, StaffTag
from qgendapy.odata import OData
from qgendapy.resources.staff import StaffResource


def _mock_client(response_data, status_code=200):
    client = MagicMock()
    client.company_key = "test-key"
    resp = httpx.Response(
        status_code,
        json=response_data,
        request=httpx.Request("GET", "http://test"),
    )
    client._transport.request.return_value = resp
    return client


class TestStaffList:
    def test_returns_staff_members(self):
        data = [{"StaffKey": "s1", "FirstName": "Jane", "LastName": "Doe"}]
        client = _mock_client(data)
        resource = StaffResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], StaffMember)
        assert resp.items[0].first_name == "Jane"

    def test_includes_company_key(self):
        client = _mock_client([])
        resource = StaffResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["companyKey"] == "test-key"

    def test_odata_support(self):
        client = _mock_client([])
        resource = StaffResource(client)
        odata = OData().filter("IsActive eq true")
        resource.list(odata=odata)

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert "$filter" in params


class TestStaffGet:
    def test_gets_single_staff(self):
        data = {"StaffKey": "s1", "FirstName": "Jane"}
        client = _mock_client(data)
        resource = StaffResource(client)
        resp = resource.get("s1")

        assert len(resp.items) == 1
        assert resp.items[0].staff_key == "s1"

    def test_hits_correct_path(self):
        client = _mock_client({})
        resource = StaffResource(client)
        resource.get("s1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/staffmember/s1"


class TestStaffCreate:
    def test_posts_data(self):
        client = _mock_client({"StaffKey": "s-new"})
        resource = StaffResource(client)
        resource.create(data={"FirstName": "New"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/staffmember"


class TestStaffUpdate:
    def test_puts_data(self):
        client = _mock_client({"StaffKey": "s1"})
        resource = StaffResource(client)
        resource.update("s1", data={"FirstName": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/staffmember/s1"


class TestStaffTags:
    def test_returns_tags(self):
        data = [{"TagKey": "t1", "TagName": "Radiology"}]
        client = _mock_client(data)
        resource = StaffResource(client)
        resp = resource.tags("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], StaffTag)

    def test_add_tag(self):
        client = _mock_client({"TagKey": "t1"})
        resource = StaffResource(client)
        resource.add_tag("s1", data={"TagKey": "t1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/staffmember/s1/tag"


class TestStaffSkillsets:
    def test_returns_skillsets(self):
        data = [{"TaskKey": "tk1", "TaskName": "CT", "Level": 3}]
        client = _mock_client(data)
        resource = StaffResource(client)
        resp = resource.skillsets("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], StaffSkillset)
        assert resp.items[0].level == 3

    def test_delete_skillset(self):
        client = _mock_client("")
        resource = StaffResource(client)
        resource.delete_skillset("s1", "tk1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/staffmember/s1/skillset/tk1"


class TestStaffPayModifiers:
    def test_returns_pay_modifiers(self):
        data = [{"PayModifierKey": "pm1", "Amount": 50.0}]
        client = _mock_client(data)
        resource = StaffResource(client)
        resp = resource.pay_modifiers("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], PayModifier)

    def test_create_pay_modifier(self):
        client = _mock_client({"PayModifierKey": "pm-new"})
        resource = StaffResource(client)
        resource.create_pay_modifier("s1", data={"Amount": 100})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"

    def test_delete_pay_modifier(self):
        client = _mock_client("")
        resource = StaffResource(client)
        resource.delete_pay_modifier("s1", "pm1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/staffmember/s1/payModifier/pm1"


class TestStaffMisc:
    def test_badge_id(self):
        client = _mock_client({})
        resource = StaffResource(client)
        resource.badge_id("s1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/staffmember/s1/badgeId"

    def test_request_limits(self):
        client = _mock_client({})
        resource = StaffResource(client)
        resource.request_limits("s1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/staffmember/s1/requestlimit"

    def test_set_manager(self):
        client = _mock_client({})
        resource = StaffResource(client)
        resource.set_manager("s1", data={"ManagerKey": "m1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/staffmember/s1/manager"
