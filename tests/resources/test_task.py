from unittest.mock import MagicMock

import httpx

from qgendapy.models.task import Task, TaskShift
from qgendapy.odata import OData
from qgendapy.resources.task import TaskResource


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


class TestTaskList:
    def test_returns_tasks(self):
        data = [{"TaskKey": "t1", "TaskName": "CT Reading", "IsActive": True}]
        client = _mock_client(data)
        resource = TaskResource(client)
        resp = resource.list()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], Task)
        assert resp.items[0].task_name == "CT Reading"

    def test_odata_support(self):
        client = _mock_client([])
        resource = TaskResource(client)
        odata = OData().select("TaskKey", "TaskName")
        resource.list(odata=odata)

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert "$select" in params


class TestTaskCreate:
    def test_posts_data(self):
        client = _mock_client({"TaskKey": "t-new"})
        resource = TaskResource(client)
        resource.create(data={"TaskName": "New Task"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/task"


class TestTaskUpdate:
    def test_puts_data(self):
        client = _mock_client({"TaskKey": "t1"})
        resource = TaskResource(client)
        resource.update(data={"TaskKey": "t1", "TaskName": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/task"


class TestTaskShifts:
    def test_returns_shifts(self):
        data = [{"TaskShiftKey": "ts1", "ShiftName": "Morning"}]
        client = _mock_client(data)
        resource = TaskResource(client)
        resp = resource.shifts("t1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], TaskShift)

    def test_create_shift(self):
        client = _mock_client({"TaskShiftKey": "ts-new"})
        resource = TaskResource(client)
        resource.create_shift("t1", data={"ShiftName": "Night"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/task/t1/taskshift"

    def test_update_shift(self):
        client = _mock_client({"TaskShiftKey": "ts1"})
        resource = TaskResource(client)
        resource.update_shift("t1", "ts1", data={"ShiftName": "Evening"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/task/t1/taskshift/ts1"

    def test_delete_shift(self):
        client = _mock_client("")
        resource = TaskResource(client)
        resource.delete_shift("t1", "ts1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/task/t1/taskshift/ts1"


class TestTaskSubresources:
    def test_locations(self):
        client = _mock_client([])
        resource = TaskResource(client)
        resource.locations("t1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/task/t1/location"

    def test_tags(self):
        client = _mock_client([])
        resource = TaskResource(client)
        resource.tags("t1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/task/t1/tag"

    def test_add_tag(self):
        client = _mock_client({})
        resource = TaskResource(client)
        resource.add_tag("t1", data={"TagKey": "tg1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/task/t1/tag"
