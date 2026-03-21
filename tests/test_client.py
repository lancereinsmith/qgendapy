from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from qgendapy._cache import NullCache
from qgendapy.client import AsyncQGendaClient, QGendaClient
from qgendapy.resources.company import AsyncCompanyResource, CompanyResource
from qgendapy.resources.credentialing import (
    AsyncCredentialingResource,
    CredentialingResource,
)
from qgendapy.resources.schedule import AsyncScheduleResource, ScheduleResource
from qgendapy.resources.staff import AsyncStaffResource, StaffResource
from qgendapy.resources.task import AsyncTaskResource, TaskResource


@patch("qgendapy.client.Auth")
@patch("qgendapy.client.Transport")
class TestQGendaClientInit:
    def test_creates_transport_and_auth(self, MockTransport, MockAuth):
        client = QGendaClient(email="a@b.com", password="pw", company_key="ck")
        MockAuth.assert_called_once()
        MockTransport.assert_called_once()
        assert client._auth is MockAuth.return_value
        assert client._transport is MockTransport.return_value

    def test_company_key_property(self, MockTransport, MockAuth):
        client = QGendaClient(email="a@b.com", password="pw", company_key="ck")
        assert client.company_key == "ck"

    def test_default_cache_is_null(self, MockTransport, MockAuth):
        client = QGendaClient(email="a@b.com", password="pw", company_key="ck")
        assert isinstance(client._cache, NullCache)

    def test_custom_cache(self, MockTransport, MockAuth):
        cache = MagicMock()
        client = QGendaClient(email="a@b.com", password="pw", company_key="ck", cache=cache)
        assert client._cache is cache

    def test_resources_attached(self, MockTransport, MockAuth):
        client = QGendaClient(email="a@b.com", password="pw", company_key="ck")
        assert isinstance(client.schedule, ScheduleResource)
        assert isinstance(client.staff, StaffResource)
        assert isinstance(client.task, TaskResource)
        assert isinstance(client.company, CompanyResource)
        assert isinstance(client.credentialing, CredentialingResource)


@patch("qgendapy.client.Auth")
@patch("qgendapy.client.Transport")
class TestQGendaClientContextManager:
    def test_close_calls_transport_close(self, MockTransport, MockAuth):
        client = QGendaClient(email="a@b.com", password="pw", company_key="ck")
        client.close()
        client._transport.close.assert_called_once()

    def test_context_manager_returns_self(self, MockTransport, MockAuth):
        client = QGendaClient(email="a@b.com", password="pw", company_key="ck")
        with client as ctx:
            assert ctx is client

    def test_context_manager_closes_on_exit(self, MockTransport, MockAuth):
        with QGendaClient(email="a@b.com", password="pw", company_key="ck") as client:
            pass
        client._transport.close.assert_called_once()


@patch("qgendapy.client.AsyncAuth")
@patch("qgendapy.client.AsyncTransport")
class TestAsyncQGendaClientInit:
    def test_creates_transport_and_auth(self, MockTransport, MockAuth):
        AsyncQGendaClient(email="a@b.com", password="pw", company_key="ck")
        MockAuth.assert_called_once()
        MockTransport.assert_called_once()

    def test_company_key_property(self, MockTransport, MockAuth):
        client = AsyncQGendaClient(email="a@b.com", password="pw", company_key="ck")
        assert client.company_key == "ck"

    def test_resources_are_async(self, MockTransport, MockAuth):
        client = AsyncQGendaClient(email="a@b.com", password="pw", company_key="ck")
        assert isinstance(client.schedule, AsyncScheduleResource)
        assert isinstance(client.staff, AsyncStaffResource)
        assert isinstance(client.task, AsyncTaskResource)
        assert isinstance(client.company, AsyncCompanyResource)
        assert isinstance(client.credentialing, AsyncCredentialingResource)


@patch("qgendapy.client.AsyncAuth")
@patch("qgendapy.client.AsyncTransport")
class TestAsyncQGendaClientContextManager:
    @pytest.mark.asyncio
    async def test_close_calls_transport_close(self, MockTransport, MockAuth):
        client = AsyncQGendaClient(email="a@b.com", password="pw", company_key="ck")
        client._transport.close = AsyncMock()
        await client.close()
        client._transport.close.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_context_manager_returns_self(self, MockTransport, MockAuth):
        client = AsyncQGendaClient(email="a@b.com", password="pw", company_key="ck")
        client._transport.close = AsyncMock()
        async with client as ctx:
            assert ctx is client

    @pytest.mark.asyncio
    async def test_context_manager_closes_on_exit(self, MockTransport, MockAuth):
        MockTransport.return_value.close = AsyncMock()
        async with AsyncQGendaClient(email="a@b.com", password="pw", company_key="ck") as client:
            pass
        client._transport.close.assert_awaited_once()
