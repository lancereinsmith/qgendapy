from unittest.mock import MagicMock

import httpx

from qgendapy.models.request import ApprovedRequest, Request
from qgendapy.resources.request import RequestResource


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


class TestRequestList:
    def test_returns_requests(self):
        data = [{"RequestKey": "rk1", "StaffKey": "sk1", "Status": "Pending"}]
        client = _mock_client(data)
        resource = RequestResource(client)
        resp = resource.list(start_date="2024-01-01")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Request)
        assert resp.items[0].request_key == "rk1"
        assert resp.items[0].status == "Pending"

    def test_passes_required_params(self):
        client = _mock_client([])
        resource = RequestResource(client)
        resource.list(start_date="2024-01-01")

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["startDate"] == "2024-01-01"
        assert params["companyKey"] == "test-key"

    def test_passes_optional_params(self):
        client = _mock_client([])
        resource = RequestResource(client)
        resource.list(start_date="2024-01-01", end_date="2024-01-31", include_removed=True)

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["endDate"] == "2024-01-31"
        assert params["includeRemoved"] == "true"


class TestRequestApproved:
    def test_returns_approved_requests(self):
        data = [{"RequestKey": "rk1", "Status": "Approved"}]
        client = _mock_client(data)
        resource = RequestResource(client)
        resp = resource.approved(start_date="2024-01-01")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], ApprovedRequest)

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = RequestResource(client)
        resource.approved()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/request/approved"
