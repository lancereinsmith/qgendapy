from unittest.mock import MagicMock

import httpx

from qgendapy.resources.support import SupportResource


def _mock_client(response_data, status_code=200):
    client = MagicMock()
    client.company_key = "test-key"
    resp = httpx.Response(
        status_code,
        json=response_data,
        request=httpx.Request("POST", "http://test"),
    )
    client._transport.request.return_value = resp
    return client


class TestSupportSendMessage:
    def test_hits_correct_path(self):
        client = _mock_client({})
        resource = SupportResource(client)
        resource.send_message("sk1", data={"Message": "Hello"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/support/staff/sk1"

    def test_passes_json_data(self):
        client = _mock_client({})
        resource = SupportResource(client)
        resource.send_message("sk1", data={"Message": "Hello"})

        call_args = client._transport.request.call_args
        assert call_args.kwargs.get("json") == {"Message": "Hello"}
