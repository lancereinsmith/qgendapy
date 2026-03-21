from unittest.mock import MagicMock

import httpx

from qgendapy.models.facility import Facility
from qgendapy.odata import OData
from qgendapy.resources.facility import FacilityResource


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


class TestFacilityList:
    def test_returns_facilities(self):
        data = [{"LocationKey": "loc1", "FacilityName": "Main Hospital"}]
        client = _mock_client(data)
        resource = FacilityResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Facility)
        assert resp.items[0].facility_name == "Main Hospital"

    def test_uses_location_path(self):
        client = _mock_client([])
        resource = FacilityResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/location"

    def test_odata_support(self):
        client = _mock_client([])
        resource = FacilityResource(client)
        odata = OData().filter("IsActive eq true")
        resource.list(odata=odata)

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert "$filter" in params


class TestFacilityGet:
    def test_gets_single(self):
        data = {"LocationKey": "loc1", "FacilityName": "Main"}
        client = _mock_client(data)
        resource = FacilityResource(client)
        resp = resource.get("loc1")

        assert resp.items[0].location_key == "loc1"


class TestFacilityCRUD:
    def test_create(self):
        client = _mock_client({"LocationKey": "loc-new"})
        resource = FacilityResource(client)
        resource.create(data={"FacilityName": "New"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"

    def test_update(self):
        client = _mock_client({"LocationKey": "loc1"})
        resource = FacilityResource(client)
        resource.update("loc1", data={"FacilityName": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/location/loc1"

    def test_delete(self):
        client = _mock_client("")
        resource = FacilityResource(client)
        resource.delete("loc1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/location/loc1"


class TestFacilityStaff:
    def test_staff(self):
        client = _mock_client([])
        resource = FacilityResource(client)
        resource.staff("loc1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/location/loc1/staff"

    def test_add_staff(self):
        client = _mock_client({})
        resource = FacilityResource(client)
        resource.add_staff("loc1", data={"StaffKey": "s1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"

    def test_remove_staff(self):
        client = _mock_client("")
        resource = FacilityResource(client)
        resource.remove_staff("loc1", "s1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/location/loc1/staff/s1"

    def test_staff_fte(self):
        client = _mock_client({})
        resource = FacilityResource(client)
        resource.staff_fte("loc1", "s1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/location/loc1/staff/s1/FTE"


class TestFacilityTasks:
    def test_tasks(self):
        client = _mock_client([])
        resource = FacilityResource(client)
        resource.tasks("loc1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/location/loc1/tasks"

    def test_add_task(self):
        client = _mock_client({})
        resource = FacilityResource(client)
        resource.add_task("loc1", data={"TaskKey": "t1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/location/loc1/task"

    def test_remove_task(self):
        client = _mock_client("")
        resource = FacilityResource(client)
        resource.remove_task("loc1", "t1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/location/loc1/task/t1"
