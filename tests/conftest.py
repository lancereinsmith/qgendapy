from unittest.mock import MagicMock

import pytest

from qgendapy._auth import Auth
from qgendapy._config import QGendaConfig
from qgendapy._transport import Transport


@pytest.fixture
def mock_config():
    return QGendaConfig(email="test@example.com", password="secret", company_key="abc123")


@pytest.fixture
def mock_auth(mock_config):
    auth = MagicMock(spec=Auth)
    auth.token = "fake-token"
    return auth


@pytest.fixture
def mock_transport(mock_auth):
    transport = MagicMock(spec=Transport)
    return transport
