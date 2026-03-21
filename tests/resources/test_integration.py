from unittest.mock import MagicMock

import httpx

from qgendapy.resources.integration import IntegrationResource


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


class TestIntegrationUploadFile:
    def test_hits_correct_path(self):
        client = _mock_client({})
        resource = IntegrationResource(client)
        resource.upload_file(files={"file": ("test.csv", b"data")})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/Integration/File"

    def test_passes_files_and_data(self):
        client = _mock_client({})
        resource = IntegrationResource(client)
        files = {"file": ("test.csv", b"data")}
        resource.upload_file(files=files, data={"key": "value"})

        call_args = client._transport.request.call_args
        assert call_args.kwargs.get("files") == files
        assert call_args.kwargs.get("data") == {"key": "value"}
