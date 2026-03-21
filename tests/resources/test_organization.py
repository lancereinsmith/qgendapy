from unittest.mock import MagicMock

import httpx

from qgendapy.models.organization import Organization
from qgendapy.resources.organization import OrganizationResource


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


class TestOrganizationList:
    def test_returns_organizations(self):
        data = [{"OrganizationKey": "org1", "OrganizationName": "Acme Health"}]
        client = _mock_client(data)
        resource = OrganizationResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Organization)
        assert resp.items[0].organization_name == "Acme Health"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = OrganizationResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/organization"

    def test_includes_company_key(self):
        client = _mock_client([])
        resource = OrganizationResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert params["companyKey"] == "test-key"
