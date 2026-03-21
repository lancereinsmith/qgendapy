from unittest.mock import MagicMock

import httpx

from qgendapy.models.time_event import TimeEvent
from qgendapy.resources.time_event import TimeEventResource


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


class TestTimeEventList:
    def test_returns_time_events(self):
        data = [{"TimeEventKey": "te1", "Hours": 8.0, "StaffFName": "John"}]
        client = _mock_client(data)
        resource = TimeEventResource(client)
        resp = resource.list(start_date="2024-01-01")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], TimeEvent)
        assert resp.items[0].hours == 8.0

    def test_passes_required_params(self):
        client = _mock_client([])
        resource = TimeEventResource(client)
        resource.list(start_date="2024-01-01")

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["startDate"] == "2024-01-01"
        assert params["companyKey"] == "test-key"


class TestTimeEventCRUD:
    def test_create(self):
        client = _mock_client({"TimeEventKey": "te-new"})
        resource = TimeEventResource(client)
        resource.create(data={"Hours": 4})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/timeevent"

    def test_update(self):
        client = _mock_client({"TimeEventKey": "te1"})
        resource = TimeEventResource(client)
        resource.update("te1", data={"Hours": 10})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/timeevent/te1"

    def test_delete(self):
        client = _mock_client("")
        resource = TimeEventResource(client)
        resource.delete("te1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/timeevent/te1"
