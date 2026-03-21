from unittest.mock import MagicMock

import httpx

from qgendapy.resources.notification import NotificationResource


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


class TestNotificationList:
    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = NotificationResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/notificationlist"


class TestNotificationCRUD:
    def test_create(self):
        client = _mock_client({})
        resource = NotificationResource(client)
        resource.create(data={"Name": "My List"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/notificationlist"

    def test_get(self):
        client = _mock_client({})
        resource = NotificationResource(client)
        resource.get("nlk1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/notificationlist/nlk1"

    def test_update(self):
        client = _mock_client({})
        resource = NotificationResource(client)
        resource.update("nlk1", data={"Name": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/notificationlist/nlk1"

    def test_delete(self):
        client = _mock_client("")
        resource = NotificationResource(client)
        resource.delete("nlk1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/notificationlist/nlk1"


class TestNotificationContacts:
    def test_contacts_path(self):
        client = _mock_client([])
        resource = NotificationResource(client)
        resource.contacts("nlk1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/notificationlist/nlk1/contact"

    def test_add_contact(self):
        client = _mock_client({})
        resource = NotificationResource(client)
        resource.add_contact("nlk1", data={"Email": "test@test.com"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/notificationlist/nlk1/contact"

    def test_update_contact(self):
        client = _mock_client({})
        resource = NotificationResource(client)
        resource.update_contact("nlk1", data={"Email": "new@test.com"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"

    def test_remove_contact(self):
        client = _mock_client("")
        resource = NotificationResource(client)
        resource.remove_contact("nlk1", data={"Email": "test@test.com"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/notificationlist/nlk1/contact"
