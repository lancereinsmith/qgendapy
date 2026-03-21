class QGendaError(Exception):
    """Base exception for all qgendapy errors."""


class AuthenticationError(QGendaError):
    """Raised when authentication fails."""


class APIError(QGendaError):
    """Raised when the QGenda API returns a 4xx/5xx response."""

    def __init__(
        self,
        status_code: int,
        message: str,
        response_body: str | dict | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(f"[{status_code}] {message}")


class ConfigurationError(QGendaError):
    """Raised when required configuration is missing or invalid."""


class ODataError(QGendaError):
    """Raised when an OData query is malformed."""
