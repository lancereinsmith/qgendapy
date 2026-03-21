from dataclasses import dataclass
from unittest.mock import MagicMock

import httpx
import pytest

from qgendapy.exceptions import APIError
from qgendapy.models.common import BaseModel
from qgendapy.response import QGendaResponse


def _make_response(status_code=200, json_data=None, text="", reason_phrase="OK"):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.text = text
    resp.reason_phrase = reason_phrase
    resp.headers = {"content-type": "application/json"}
    if json_data is not None:
        resp.json.return_value = json_data
    else:
        resp.json.side_effect = ValueError("No JSON")
    return resp


@dataclass
class SampleModel(BaseModel):
    name: str = ""
    email: str = ""


class TestQGendaResponseFromHttpx:
    def test_list_response_without_model(self):
        resp = _make_response(json_data=[{"Name": "A"}, {"Name": "B"}])
        result = QGendaResponse.from_httpx(resp)
        assert result.status_code == 200
        assert result.data == [{"Name": "A"}, {"Name": "B"}]
        assert result.items == []

    def test_list_response_with_model(self):
        resp = _make_response(json_data=[{"Name": "Alice", "Email": "a@b.com"}])
        result = QGendaResponse.from_httpx(resp, model=SampleModel)
        assert len(result.items) == 1
        assert result.items[0].name == "Alice"
        assert result.items[0].email == "a@b.com"

    def test_dict_response_with_model(self):
        resp = _make_response(json_data={"Name": "Bob", "Email": "b@c.com"})
        result = QGendaResponse.from_httpx(resp, model=SampleModel)
        assert len(result.items) == 1
        assert result.items[0].name == "Bob"

    def test_error_status_raises_api_error(self):
        resp = _make_response(
            status_code=404, json_data={"error": "not found"}, reason_phrase="Not Found"
        )
        with pytest.raises(APIError) as exc_info:
            QGendaResponse.from_httpx(resp)
        assert exc_info.value.status_code == 404
        assert exc_info.value.response_body == {"error": "not found"}

    def test_error_status_with_non_json_body(self):
        resp = _make_response(status_code=500, reason_phrase="Internal Server Error")
        resp.json.side_effect = ValueError("not json")
        resp.text = "server error"
        with pytest.raises(APIError) as exc_info:
            QGendaResponse.from_httpx(resp)
        assert exc_info.value.status_code == 500
        assert exc_info.value.response_body == "server error"

    def test_empty_json_body(self):
        resp = _make_response(status_code=200)
        resp.json.side_effect = ValueError("empty")
        result = QGendaResponse.from_httpx(resp)
        assert result.data == {}


class TestQGendaResponseDunder:
    def test_iter(self):
        qr = QGendaResponse(data=[], status_code=200, headers={}, items=["a", "b"])
        assert list(qr) == ["a", "b"]

    def test_len(self):
        qr = QGendaResponse(data=[], status_code=200, headers={}, items=[1, 2, 3])
        assert len(qr) == 3

    def test_bool_true(self):
        qr = QGendaResponse(data=[], status_code=200, headers={})
        assert bool(qr) is True

    def test_bool_false(self):
        qr = QGendaResponse(data=[], status_code=400, headers={})
        assert bool(qr) is False
