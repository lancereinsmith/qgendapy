from unittest.mock import MagicMock

import httpx

from qgendapy.models.common import Tag
from qgendapy.resources.tag import TagResource


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


class TestTagList:
    def test_returns_tags(self):
        data = [{"TagKey": "tk1", "TagName": "Urgent", "CategoryName": "Priority"}]
        client = _mock_client(data)
        resource = TagResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Tag)
        assert resp.items[0].tag_name == "Urgent"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = TagResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/tags"
