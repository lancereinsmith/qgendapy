"""Configuration via environment variables, INI config file, or explicit arguments.

qgendapy resolves credentials in this order:
  1. Explicit arguments passed to QGendaClient()
  2. Environment variables
  3. INI config file pointed to by QGENDA_CONF_FILE env var
"""

from qgendapy import QGendaClient

# --- Option 1: Environment variables ---
#
# Set these in your shell or .env file:
#
#   export QGENDA_EMAIL="you@hospital.org"
#   export QGENDA_PASSWORD="your-password"
#   export QGENDA_COMPANY_KEY="your-company-key"
#
# Then create the client with no arguments:

client = QGendaClient()

# --- Option 2: INI config file ---
#
# Set the path to the config file:
#
#   export QGENDA_CONF_FILE="/path/to/qgenda.conf"
#
# INI file format (compatible with legacy python-qgenda):
#
#   [qgenda]
#   username = you@hospital.org
#   password = your-password
#   company_key = your-company-key
#   api_url = https://api.qgenda.com
#   api_version = v2
#
# Use a different section with:
#
#   export QGENDA_CONF_REGION="production"

# --- Option 3: Explicit arguments override everything ---

client = QGendaClient(
    email="override@hospital.org",
    password="override-password",
    company_key="override-key",
    base_url="https://api.qgenda.com/v2",
)

client.close()
