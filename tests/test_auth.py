import threading
from unittest.mock import MagicMock, patch

import httpx
import pytest

from qgendapy._auth import AsyncAuth, Auth
from qgendapy.exceptions import AuthenticationError


def _make_login_response(status_code=200, access_token="tok123", expires_in=3600):
    """Create a mock httpx.Response for login."""
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.text = "error" if status_code != 200 else ""
    resp.json.return_value = {"access_token": access_token, "expires_in": expires_in}
    return resp


class TestAuth:
    @patch("qgendapy._auth.httpx.Client")
    def test_token_triggers_refresh(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = _make_login_response()

        auth = Auth(email="a@b.com", password="pw", base_url="https://api.test.com")
        token = auth.token

        assert token == "tok123"
        mock_client.post.assert_called_once()

    @patch("qgendapy._auth.httpx.Client")
    def test_token_cached_when_not_expired(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = _make_login_response()

        auth = Auth(email="a@b.com", password="pw", base_url="https://api.test.com")
        _ = auth.token
        _ = auth.token  # second call should not trigger refresh

        assert mock_client.post.call_count == 1

    @patch("qgendapy._auth.httpx.Client")
    def test_token_refreshes_when_expired(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = _make_login_response(expires_in=1)

        auth = Auth(email="a@b.com", password="pw", base_url="https://api.test.com")
        # expires_in=1 with 60s buffer means it's already "expired"
        _ = auth.token
        _ = auth.token

        assert mock_client.post.call_count == 2

    @patch("qgendapy._auth.httpx.Client")
    def test_login_failure_raises(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = _make_login_response(status_code=401)

        auth = Auth(email="a@b.com", password="pw", base_url="https://api.test.com")
        with pytest.raises(AuthenticationError, match="401"):
            _ = auth.token

    @patch("qgendapy._auth.httpx.Client")
    def test_thread_safety(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = _make_login_response()

        auth = Auth(email="a@b.com", password="pw", base_url="https://api.test.com")
        results = []

        def get_token():
            results.append(auth.token)

        threads = [threading.Thread(target=get_token) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 10
        assert all(r == "tok123" for r in results)


def _make_async_client_mock(post_response):
    """Create a mock that works as an async context manager returning a client with .post()."""
    mock_client = MagicMock()

    async def mock_post(*args, **kwargs):
        return post_response

    mock_client.post = mock_post

    class FakeAsyncClient:
        async def __aenter__(self):
            return mock_client

        async def __aexit__(self, *args):
            pass

    return FakeAsyncClient


class TestAsyncAuth:
    @pytest.mark.asyncio
    @patch("qgendapy._auth.httpx.AsyncClient")
    async def test_get_token_triggers_refresh(self, mock_client_cls):
        mock_client_cls.side_effect = lambda: _make_async_client_mock(_make_login_response())()

        auth = AsyncAuth(email="a@b.com", password="pw", base_url="https://api.test.com")
        token = await auth.get_token()

        assert token == "tok123"

    @pytest.mark.asyncio
    @patch("qgendapy._auth.httpx.AsyncClient")
    async def test_login_failure_raises(self, mock_client_cls):
        mock_client_cls.side_effect = lambda: _make_async_client_mock(
            _make_login_response(status_code=401)
        )()

        auth = AsyncAuth(email="a@b.com", password="pw", base_url="https://api.test.com")
        with pytest.raises(AuthenticationError, match="401"):
            await auth.get_token()
