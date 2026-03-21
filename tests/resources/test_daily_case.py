from unittest.mock import MagicMock

import httpx

from qgendapy.models.daily import DailyCase
from qgendapy.resources.daily_case import DailyCaseResource


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


class TestDailyCaseList:
    def test_returns_daily_cases(self):
        data = [{"DailyCaseKey": "dc1", "CaseCount": 5, "StaffFName": "Jane"}]
        client = _mock_client(data)
        resource = DailyCaseResource(client)
        resp = resource.list(start_date="2024-01-01")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], DailyCase)
        assert resp.items[0].case_count == 5

    def test_passes_required_params(self):
        client = _mock_client([])
        resource = DailyCaseResource(client)
        resource.list(start_date="2024-01-01")

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["startDate"] == "2024-01-01"
        assert params["companyKey"] == "test-key"


class TestDailyCaseCRUD:
    def test_create(self):
        client = _mock_client({"DailyCaseKey": "dc-new"})
        resource = DailyCaseResource(client)
        resource.create(data={"CaseCount": 3})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/dailycase"

    def test_update(self):
        client = _mock_client({"DailyCaseKey": "dc1"})
        resource = DailyCaseResource(client)
        resource.update("dc1", data={"CaseCount": 10})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/dailycase/dc1"

    def test_delete(self):
        client = _mock_client("")
        resource = DailyCaseResource(client)
        resource.delete("dc1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/dailycase/dc1"
