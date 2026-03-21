from unittest.mock import MagicMock

import httpx

from qgendapy.models.company import Company
from qgendapy.resources.company import CompanyResource


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


class TestCompanyList:
    def test_returns_companies(self):
        data = [{"CompanyKey": "ck1", "CompanyName": "Acme Health"}]
        client = _mock_client(data)
        resource = CompanyResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Company)
        assert resp.items[0].company_name == "Acme Health"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = CompanyResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/company"
