from unittest.mock import MagicMock

import httpx

from qgendapy.models.staff import StaffType
from qgendapy.resources.staff_type import StaffTypeResource


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


class TestStaffTypeList:
    def test_returns_staff_types(self):
        data = [
            {"StaffTypeKey": "stk1", "StaffTypeName": "Shareholder", "IsActive": True},
            {"StaffTypeKey": "stk2", "StaffTypeName": "Locum", "IsActive": True},
        ]
        client = _mock_client(data)
        resource = StaffTypeResource(client)
        resp = resource.list()

        assert len(resp.items) == 2
        assert isinstance(resp.items[0], StaffType)
        assert resp.items[0].staff_type_name == "Shareholder"
        assert resp.items[1].staff_type_name == "Locum"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = StaffTypeResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/stafftype"
