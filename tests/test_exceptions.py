import pytest

from qgendapy.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    ODataError,
    QGendaError,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_qgenda_error(self):
        assert issubclass(AuthenticationError, QGendaError)
        assert issubclass(APIError, QGendaError)
        assert issubclass(ConfigurationError, QGendaError)
        assert issubclass(ODataError, QGendaError)

    def test_qgenda_error_is_exception(self):
        assert issubclass(QGendaError, Exception)

    def test_catch_all_with_qgenda_error(self):
        with pytest.raises(QGendaError):
            raise AuthenticationError("bad creds")

        with pytest.raises(QGendaError):
            raise APIError(500, "server error")

        with pytest.raises(QGendaError):
            raise ConfigurationError("missing key")

        with pytest.raises(QGendaError):
            raise ODataError("bad filter")


class TestAPIError:
    def test_attributes(self):
        err = APIError(status_code=422, message="Validation failed", response_body={"x": 1})
        assert err.status_code == 422
        assert err.message == "Validation failed"
        assert err.response_body == {"x": 1}

    def test_str_format(self):
        err = APIError(status_code=404, message="Not Found")
        assert str(err) == "[404] Not Found"

    def test_response_body_default_none(self):
        err = APIError(status_code=500, message="Error")
        assert err.response_body is None

    def test_response_body_string(self):
        err = APIError(status_code=500, message="Error", response_body="raw text")
        assert err.response_body == "raw text"
