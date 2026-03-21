from unittest.mock import MagicMock

import httpx

from qgendapy.resources.staff_target import StaffTargetResource


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


class TestStaffTargetList:
    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = StaffTargetResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/stafftarget"


class TestStaffTargetCRUD:
    def test_create(self):
        client = _mock_client({})
        resource = StaffTargetResource(client)
        resource.create(data={"Name": "Target"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/stafftarget"

    def test_update(self):
        client = _mock_client({})
        resource = StaffTargetResource(client)
        resource.update(data={"Name": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"

    def test_delete_body_based(self):
        client = _mock_client("")
        resource = StaffTargetResource(client)
        resource.delete(data={"StaffTargetKey": "stk1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/stafftarget"


class TestStaffTargetLocations:
    def test_locations_path(self):
        client = _mock_client([])
        resource = StaffTargetResource(client)
        resource.locations("stk1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/stafftarget/stk1/location"

    def test_add_location(self):
        client = _mock_client({})
        resource = StaffTargetResource(client)
        resource.add_location("stk1", "loc1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/stafftarget/stk1/location/loc1"

    def test_remove_location(self):
        client = _mock_client("")
        resource = StaffTargetResource(client)
        resource.remove_location("stk1", "loc1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/stafftarget/stk1/location/loc1"


class TestStaffTargetStaff:
    def test_staff_path(self):
        client = _mock_client([])
        resource = StaffTargetResource(client)
        resource.staff("stk1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/stafftarget/stk1/staff"

    def test_add_staff(self):
        client = _mock_client({})
        resource = StaffTargetResource(client)
        resource.add_staff("stk1", "sk1", data={"Weight": 1.0})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/stafftarget/stk1/staff/sk1"

    def test_remove_staff(self):
        client = _mock_client("")
        resource = StaffTargetResource(client)
        resource.remove_staff("stk1", "sk1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"


class TestStaffTargetTaskShifts:
    def test_task_shifts_path(self):
        client = _mock_client([])
        resource = StaffTargetResource(client)
        resource.task_shifts("stk1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/stafftarget/stk1/taskshift"

    def test_add_task_shift(self):
        client = _mock_client({})
        resource = StaffTargetResource(client)
        resource.add_task_shift("stk1", data={"TaskKey": "tk1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"

    def test_remove_task_shift(self):
        client = _mock_client("")
        resource = StaffTargetResource(client)
        resource.remove_task_shift("stk1", "tsk1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/stafftarget/stk1/taskshift/tsk1"
