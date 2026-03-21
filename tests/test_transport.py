from unittest.mock import MagicMock, patch

import httpx
import pytest

from qgendapy._auth import AsyncAuth
from qgendapy._transport import AsyncTransport, Transport


class TestTransport:
    def test_request_adds_auth_header(self, mock_auth):
        with patch.object(httpx.Client, "request") as mock_request:
            mock_request.return_value = MagicMock(spec=httpx.Response)
            transport = Transport(auth=mock_auth, base_url="https://api.test.com")
            transport.request("GET", "/test")

            call_kwargs = mock_request.call_args
            assert call_kwargs.kwargs["headers"]["Authorization"] == "Bearer fake-token"

    def test_request_merges_custom_headers(self, mock_auth):
        with patch.object(httpx.Client, "request") as mock_request:
            mock_request.return_value = MagicMock(spec=httpx.Response)
            transport = Transport(auth=mock_auth, base_url="https://api.test.com")
            transport.request("GET", "/test", headers={"X-Custom": "value"})

            call_kwargs = mock_request.call_args
            assert call_kwargs.kwargs["headers"]["X-Custom"] == "value"
            assert call_kwargs.kwargs["headers"]["Authorization"] == "Bearer fake-token"

    def test_request_passes_params(self, mock_auth):
        with patch.object(httpx.Client, "request") as mock_request:
            mock_request.return_value = MagicMock(spec=httpx.Response)
            transport = Transport(auth=mock_auth, base_url="https://api.test.com")
            transport.request("GET", "/test", params={"key": "val"})

            call_kwargs = mock_request.call_args
            assert call_kwargs.kwargs["params"] == {"key": "val"}

    def test_request_passes_json(self, mock_auth):
        with patch.object(httpx.Client, "request") as mock_request:
            mock_request.return_value = MagicMock(spec=httpx.Response)
            transport = Transport(auth=mock_auth, base_url="https://api.test.com")
            transport.request("POST", "/test", json={"data": 1})

            call_kwargs = mock_request.call_args
            assert call_kwargs.kwargs["json"] == {"data": 1}

    def test_all_http_methods(self, mock_auth):
        with patch.object(httpx.Client, "request") as mock_request:
            mock_request.return_value = MagicMock(spec=httpx.Response)
            transport = Transport(auth=mock_auth, base_url="https://api.test.com")

            for method in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                transport.request(method, "/test")

            methods_called = [call.args[0] for call in mock_request.call_args_list]
            assert methods_called == ["GET", "POST", "PUT", "DELETE", "PATCH"]

    def test_close(self, mock_auth):
        with patch.object(httpx.Client, "close") as mock_close:
            transport = Transport(auth=mock_auth, base_url="https://api.test.com")
            transport.close()
            mock_close.assert_called_once()


class TestAsyncTransport:
    @pytest.mark.asyncio
    async def test_request_adds_auth_header(self):
        mock_auth = MagicMock(spec=AsyncAuth)
        mock_auth.get_token = MagicMock(return_value="async-token")

        with patch.object(httpx.AsyncClient, "request") as mock_request:
            mock_response = MagicMock(spec=httpx.Response)

            async def async_return(*args, **kwargs):
                return mock_response

            mock_request.side_effect = async_return
            mock_auth.get_token = MagicMock(side_effect=lambda: "async-token")

            # Make get_token a coroutine
            async def get_token():
                return "async-token"

            mock_auth.get_token = get_token

            transport = AsyncTransport(auth=mock_auth, base_url="https://api.test.com")
            await transport.request("GET", "/test")

            call_kwargs = mock_request.call_args
            assert call_kwargs.kwargs["headers"]["Authorization"] == "Bearer async-token"

    @pytest.mark.asyncio
    async def test_close(self):
        mock_auth = MagicMock(spec=AsyncAuth)
        with patch.object(httpx.AsyncClient, "aclose") as mock_aclose:

            async def async_aclose(*args, **kwargs):
                return None

            mock_aclose.side_effect = async_aclose

            transport = AsyncTransport(auth=mock_auth, base_url="https://api.test.com")
            await transport.close()
            mock_aclose.assert_called_once()
