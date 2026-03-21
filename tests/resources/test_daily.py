from unittest.mock import MagicMock

import httpx

from qgendapy.models.daily import (
    CapacityRoomAssignment,
    DailyConfiguration,
    PatientEncounter,
    Room,
)
from qgendapy.resources.daily import DailyResource


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


class TestDailyConfigurations:
    def test_returns_configurations(self):
        data = [{"DailyConfigurationKey": "dc1", "Name": "Default"}]
        client = _mock_client(data)
        resource = DailyResource(client)
        resp = resource.configurations()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], DailyConfiguration)
        assert resp.items[0].name == "Default"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = DailyResource(client)
        resource.configurations()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/daily/dailyconfiguration"


class TestDailyGetConfiguration:
    def test_hits_correct_path(self):
        client = _mock_client({"DailyConfigurationKey": "dc1"})
        resource = DailyResource(client)
        resource.get_configuration("dc1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/daily/dailyconfiguration/dc1"


class TestDailyRooms:
    def test_returns_rooms(self):
        data = [{"RoomKey": "r1", "RoomName": "Room A"}]
        client = _mock_client(data)
        resource = DailyResource(client)
        resp = resource.rooms()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Room)
        assert resp.items[0].room_name == "Room A"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = DailyResource(client)
        resource.rooms()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/daily/room"


class TestPatientEncounters:
    def test_returns_patient_encounters(self):
        data = [{"PatientEncounterKey": "pe1", "StaffKey": "sk1"}]
        client = _mock_client(data)
        resource = DailyResource(client)
        resp = resource.patient_encounters()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], PatientEncounter)

    def test_passes_optional_params(self):
        client = _mock_client([])
        resource = DailyResource(client)
        resource.patient_encounters(daily_configuration_key="dc1", start_date="2024-01-01")

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["dailyConfigurationKey"] == "dc1"
        assert params["startDate"] == "2024-01-01"

    def test_create(self):
        client = _mock_client({"PatientEncounterKey": "pe-new"})
        resource = DailyResource(client)
        resource.create_patient_encounter(data={"StaffKey": "sk1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/daily/patientencounter"

    def test_update(self):
        client = _mock_client({"PatientEncounterKey": "pe1"})
        resource = DailyResource(client)
        resource.update_patient_encounter(data={"StaffKey": "sk1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/daily/patientencounter"

    def test_delete(self):
        client = _mock_client("")
        resource = DailyResource(client)
        resource.delete_patient_encounter("pe1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/daily/patientencounter/pe1"


class TestCapacityRoomAssignments:
    def test_returns_assignments(self):
        data = [{"CapacityRoomAssignmentKey": "cra1", "RoomKey": "r1"}]
        client = _mock_client(data)
        resource = DailyResource(client)
        resp = resource.capacity_room_assignments()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CapacityRoomAssignment)

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = DailyResource(client)
        resource.capacity_room_assignments()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/daily/capacityroomassignment"
