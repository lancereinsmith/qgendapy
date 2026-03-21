from unittest.mock import MagicMock

import httpx

from qgendapy.resources.user import UserResource


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


class TestUserList:
    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = UserResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/user"


class TestUserGet:
    def test_hits_correct_path(self):
        client = _mock_client({})
        resource = UserResource(client)
        resource.get("uk1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/user/uk1"


class TestNonScheduledUser:
    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = UserResource(client)
        resource.non_scheduled()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/NonScheduledUser"

    def test_permissions_path(self):
        client = _mock_client([])
        resource = UserResource(client)
        resource.non_scheduled_permissions("loc1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/NonScheduledUser/location/loc1/permissions"
