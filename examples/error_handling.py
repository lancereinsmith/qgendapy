"""Handling errors from the QGenda API."""

from qgendapy import QGendaClient
from qgendapy.exceptions import APIError, AuthenticationError, ConfigurationError

# --- Configuration errors ---

try:
    # Missing credentials will raise immediately
    client = QGendaClient()
except ConfigurationError as e:
    print(f"Config error: {e}")
    print("Set QGENDA_CONF_FILE to point to your qgenda.conf file")

# --- Authentication errors ---

try:
    # Assumes QGENDA_CONF_FILE is set but credentials are invalid
    client = QGendaClient()
    client.staff.list()
except AuthenticationError as e:
    print(f"Auth failed: {e}")

# --- API errors ---

try:
    client = QGendaClient()
    client.staff.get("nonexistent-key")
except APIError as e:
    print(f"API error [{e.status_code}]: {e.message}")
    print(f"Response body: {e.response_body}")
