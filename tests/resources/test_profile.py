from unittest.mock import MagicMock

import httpx

from qgendapy.models.common import Profile
from qgendapy.resources.profile import ProfileResource


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


class TestProfileList:
    def test_returns_profiles(self):
        data = [{"ProfileKey": "pk1", "ProfileName": "Radiologist"}]
        client = _mock_client(data)
        resource = ProfileResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Profile)
        assert resp.items[0].profile_name == "Radiologist"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = ProfileResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/profile"
