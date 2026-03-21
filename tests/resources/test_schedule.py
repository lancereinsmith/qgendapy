from unittest.mock import MagicMock

import httpx

from qgendapy.models.schedule import AuditLogEntry, OpenShift, Rotation, ScheduleEntry
from qgendapy.odata import OData
from qgendapy.resources.schedule import ScheduleResource


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


class TestScheduleList:
    def test_returns_schedule_entries(self):
        data = [
            {
                "ScheduleKey": "sk1",
                "StartDate": "2024-01-01",
                "StaffFName": "John",
                "TaskName": "Reading",
            }
        ]
        client = _mock_client(data)
        resource = ScheduleResource(client)
        resp = resource.list(start_date="2024-01-01")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], ScheduleEntry)
        assert resp.items[0].schedule_key == "sk1"
        assert resp.items[0].staff_f_name == "John"

    def test_passes_required_params(self):
        client = _mock_client([])
        resource = ScheduleResource(client)
        resource.list(start_date="2024-01-01")

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["startDate"] == "2024-01-01"
        assert params["companyKey"] == "test-key"

    def test_passes_optional_params(self):
        client = _mock_client([])
        resource = ScheduleResource(client)
        resource.list(start_date="2024-01-01", end_date="2024-01-31", includes="Task")

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["endDate"] == "2024-01-31"
        assert params["includes"] == "Task"

    def test_odata_merged_into_params(self):
        client = _mock_client([])
        resource = ScheduleResource(client)
        odata = OData().select("ScheduleKey", "StartDate").filter("IsPublished eq true")
        resource.list(start_date="2024-01-01", odata=odata)

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert "$select" in params
        assert "$filter" in params


class TestScheduleAuditLog:
    def test_returns_audit_log_entries(self):
        data = [{"ScheduleKey": "sk1", "Action": "Create", "ModifiedBy": "admin"}]
        client = _mock_client(data)
        resource = ScheduleResource(client)
        resp = resource.audit_log(schedule_start_date="2024-01-01")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], AuditLogEntry)
        assert resp.items[0].action == "Create"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = ScheduleResource(client)
        resource.audit_log()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/schedule/auditLog"


class TestOpenShifts:
    def test_returns_open_shifts(self):
        data = [{"ScheduleKey": "sk1", "TaskName": "CT"}]
        client = _mock_client(data)
        resource = ScheduleResource(client)
        resp = resource.open_shifts(start_date="2024-01-01")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], OpenShift)
        assert resp.items[0].task_name == "CT"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = ScheduleResource(client)
        resource.open_shifts(start_date="2024-01-01")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/schedule/openshifts"


class TestRotations:
    def test_returns_rotations(self):
        data = [{"RotationKey": "rk1", "RotationName": "Night"}]
        client = _mock_client(data)
        resource = ScheduleResource(client)
        resp = resource.rotations()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Rotation)
        assert resp.items[0].rotation_name == "Night"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = ScheduleResource(client)
        resource.rotations()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/schedule/rotations"
