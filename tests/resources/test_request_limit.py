from unittest.mock import MagicMock

import httpx

from qgendapy.models.request import RequestLimit
from qgendapy.resources.request_limit import RequestLimitResource


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


class TestRequestLimitList:
    def test_returns_request_limits(self):
        data = [{"RequestLimitKey": "rlk1", "Name": "Vacation Limit"}]
        client = _mock_client(data)
        resource = RequestLimitResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], RequestLimit)
        assert resp.items[0].name == "Vacation Limit"

    def test_hits_correct_path(self):
        client = _mock_client([])
        resource = RequestLimitResource(client)
        resource.list()

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/requestlimit"


class TestRequestLimitCRUD:
    def test_create(self):
        client = _mock_client({"RequestLimitKey": "rlk-new"})
        resource = RequestLimitResource(client)
        resource.create(data={"Name": "New Limit"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/requestlimit"

    def test_update(self):
        client = _mock_client({"RequestLimitKey": "rlk1"})
        resource = RequestLimitResource(client)
        resource.update("rlk1", data={"Name": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/requestlimit/rlk1"

    def test_delete(self):
        client = _mock_client("")
        resource = RequestLimitResource(client)
        resource.delete("rlk1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/requestlimit/rlk1"


class TestRequestLimitStaffQuotas:
    def test_staff_quotas_path(self):
        client = _mock_client([])
        resource = RequestLimitResource(client)
        resource.staff_quotas("rlk1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/requestlimit/rlk1/staffquota"

    def test_create_staff_quota(self):
        client = _mock_client({})
        resource = RequestLimitResource(client)
        resource.create_staff_quota("rlk1", data={"Quota": 5})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/requestlimit/rlk1/staffquota"

    def test_update_staff_quota(self):
        client = _mock_client({})
        resource = RequestLimitResource(client)
        resource.update_staff_quota("rlk1", "sk1", data={"Quota": 10})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/requestlimit/rlk1/staffquota/sk1"


class TestRequestLimitTaskShifts:
    def test_task_shifts_path(self):
        client = _mock_client([])
        resource = RequestLimitResource(client)
        resource.task_shifts("rlk1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/requestlimit/rlk1/taskshift"

    def test_create_task_shift(self):
        client = _mock_client({})
        resource = RequestLimitResource(client)
        resource.create_task_shift("rlk1", data={"TaskKey": "tk1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"

    def test_delete_task_shift(self):
        client = _mock_client("")
        resource = RequestLimitResource(client)
        resource.delete_task_shift("rlk1", "tsk1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/requestlimit/rlk1/taskshift/tsk1"
