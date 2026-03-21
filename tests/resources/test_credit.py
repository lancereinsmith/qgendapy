from unittest.mock import MagicMock

import httpx

from qgendapy.resources.credit import CreditAllocationResource


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


class TestCreditAllocationQuotas:
    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = CreditAllocationResource(client)
        resource.quotas()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/CreditAllocation/Quota"


class TestCreditAllocationUpdateQuota:
    def test_update_quota(self):
        client = _mock_client({})
        resource = CreditAllocationResource(client)
        resource.update_quota("cak1", "sk1", data={"Quota": 100})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/creditallocation/cak1/quota/sk1"
