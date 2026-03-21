from unittest.mock import MagicMock

import httpx

from qgendapy.models.pay import PayCode, PayPeriodAmount, PayRate
from qgendapy.resources.pay import PayCodeResource, PayPoolResource, PayRateResource


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


class TestPayCodeList:
    def test_returns_pay_codes(self):
        data = [{"PayCodeKey": "pck1", "Name": "Overtime"}]
        client = _mock_client(data)
        resource = PayCodeResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], PayCode)
        assert resp.items[0].name == "Overtime"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = PayCodeResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/PayCode"


class TestPayRateCRUD:
    def test_list(self):
        data = [{"PayRateKey": "prk1", "Name": "Standard"}]
        client = _mock_client(data)
        resource = PayRateResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], PayRate)

    def test_create(self):
        client = _mock_client({"PayRateKey": "prk-new"})
        resource = PayRateResource(client)
        resource.create(data={"Name": "New Rate"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/payrate"

    def test_update(self):
        client = _mock_client({"PayRateKey": "prk1"})
        resource = PayRateResource(client)
        resource.update("prk1", data={"Name": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/payrate/prk1"

    def test_delete(self):
        client = _mock_client("")
        resource = PayRateResource(client)
        resource.delete("prk1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/payrate/prk1"


class TestPayPoolPeriodAmounts:
    def test_returns_period_amounts(self):
        data = [{"PayPeriodAmountKey": "ppa1", "Amount": 1000.0}]
        client = _mock_client(data)
        resource = PayPoolResource(client)
        resp = resource.period_amounts("ppt1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], PayPeriodAmount)

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = PayPoolResource(client)
        resource.period_amounts("ppt1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/PayPoolTemplate/ppt1/PayPeriodAmount"
