from unittest.mock import patch

from qgendapy.compat import QGendaClient, _CompatResponse
from qgendapy.response import QGendaResponse


def _make_qgenda_response(data, status_code=200):
    return QGendaResponse(data=data, status_code=status_code, headers={"x-test": "1"})


class TestCompatResponse:
    def test_status_code(self):
        qr = _make_qgenda_response([{"a": 1}])
        resp = _CompatResponse(qr)
        assert resp.status_code == 200

    def test_json(self):
        qr = _make_qgenda_response([{"a": 1}])
        resp = _CompatResponse(qr)
        assert resp.json() == [{"a": 1}]

    def test_text(self):
        qr = _make_qgenda_response({"key": "val"})
        resp = _CompatResponse(qr)
        assert '"key"' in resp.text
        assert '"val"' in resp.text

    def test_headers(self):
        qr = _make_qgenda_response([])
        resp = _CompatResponse(qr)
        assert resp.headers["x-test"] == "1"


class TestCompatClient:
    @patch("qgendapy.compat._ModernClient")
    def test_constructor_maps_params(self, mock_cls):
        QGendaClient(
            username="user@test.com",
            password="secret",
            company_key="ck1",
            api_url="https://custom.api.com",
            api_version="v3",
        )
        mock_cls.assert_called_once_with(
            email="user@test.com",
            password="secret",
            company_key="ck1",
            base_url="https://custom.api.com/v3",
        )

    @patch("qgendapy.compat._ModernClient")
    def test_default_base_url(self, mock_cls):
        QGendaClient(username="u", password="p", company_key="ck")
        call_kwargs = mock_cls.call_args.kwargs
        assert call_kwargs["base_url"] == "https://api.qgenda.com/v2"

    @patch("qgendapy.compat._ModernClient")
    def test_authenticate_is_noop(self, mock_cls):
        client = QGendaClient(username="u", password="p", company_key="ck")
        # Should not raise
        client.authenticate()

    @patch("qgendapy.compat._ModernClient")
    def test_get_schedule_delegates(self, mock_cls):
        mock_inner = mock_cls.return_value
        mock_inner.schedule.list.return_value = _make_qgenda_response([{"ScheduleKey": "sk1"}])
        client = QGendaClient(username="u", password="p", company_key="ck")
        resp = client.get_schedule(start_date="2024-01-01", end_date="2024-01-31")

        mock_inner.schedule.list.assert_called_once()
        assert resp.status_code == 200
        assert resp.json() == [{"ScheduleKey": "sk1"}]

    @patch("qgendapy.compat._ModernClient")
    def test_get_staff_delegates(self, mock_cls):
        mock_inner = mock_cls.return_value
        mock_inner.staff.list.return_value = _make_qgenda_response([])
        client = QGendaClient(username="u", password="p", company_key="ck")
        resp = client.get_staff()

        mock_inner.staff.list.assert_called_once()
        assert resp.json() == []

    @patch("qgendapy.compat._ModernClient")
    def test_get_facility_delegates(self, mock_cls):
        mock_inner = mock_cls.return_value
        mock_inner.facility.list.return_value = _make_qgenda_response([])
        client = QGendaClient(username="u", password="p", company_key="ck")
        client.get_facility()

        mock_inner.facility.list.assert_called_once()

    @patch("qgendapy.compat._ModernClient")
    def test_get_task_delegates(self, mock_cls):
        mock_inner = mock_cls.return_value
        mock_inner.task.list.return_value = _make_qgenda_response([])
        client = QGendaClient(username="u", password="p", company_key="ck")
        client.get_task()

        mock_inner.task.list.assert_called_once()

    @patch("qgendapy.compat._ModernClient")
    def test_get_organization_delegates(self, mock_cls):
        mock_inner = mock_cls.return_value
        mock_inner.organization.list.return_value = _make_qgenda_response([])
        client = QGendaClient(username="u", password="p", company_key="ck")
        client.get_organization(organization_key="org1")

        mock_inner.organization.list.assert_called_once()

    @patch("qgendapy.compat._ModernClient")
    def test_get_timeevent_delegates(self, mock_cls):
        mock_inner = mock_cls.return_value
        mock_inner.time_event.list.return_value = _make_qgenda_response([])
        client = QGendaClient(username="u", password="p", company_key="ck")
        client.get_timeevent(start_date="2024-01-01")

        mock_inner.time_event.list.assert_called_once()

    @patch("qgendapy.compat._ModernClient")
    def test_get_dailycase_delegates(self, mock_cls):
        mock_inner = mock_cls.return_value
        mock_inner.daily_case.list.return_value = _make_qgenda_response([])
        client = QGendaClient(username="u", password="p", company_key="ck")
        client.get_dailycase(start_date="2024-01-01")

        mock_inner.daily_case.list.assert_called_once()

    @patch("qgendapy.compat._ModernClient")
    def test_odata_kwargs_passed_through(self, mock_cls):
        mock_inner = mock_cls.return_value
        mock_inner.staff.list.return_value = _make_qgenda_response([])
        client = QGendaClient(username="u", password="p", company_key="ck")
        client.get_staff(odata_kwargs={"$filter": "IsActive eq true"})

        call_kwargs = mock_inner.staff.list.call_args.kwargs
        odata = call_kwargs["odata"]
        assert odata is not None
        assert "$filter" in odata.to_params()
