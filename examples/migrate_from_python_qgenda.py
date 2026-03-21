"""Migrating from the legacy python-qgenda library.

The compat module provides a drop-in replacement. Change one import
and your existing code keeps working while you migrate incrementally.
"""

# Before (python-qgenda):
#
#   from qgenda.api.client import QGendaClient
#   client = QGendaClient(username="user@example.com", password="secret",
#                         company_key="abc123")
#   client.authenticate()
#   resp = client.get_schedule(start_date="2024-01-15")
#   data = resp.json()

# After (qgendapy compat layer -- change one import):
# Credentials are loaded from the INI file pointed to by QGENDA_CONF_FILE.

from qgendapy.compat import QGendaClient

client = QGendaClient()

# authenticate() is a no-op -- the modern client handles auth automatically
client.authenticate()

# Same method names, same return format
resp = client.get_schedule(start_date="2024-01-15", end_date="2024-01-21")
data = resp.json()
print(f"Schedule entries: {len(data)}")

# OData works the same way via odata_kwargs
resp = client.get_staff(odata_kwargs={"$filter": "IsActive eq true"})
staff = resp.json()
print(f"Active staff: {len(staff)}")

# Other legacy methods (require appropriate API permissions)
# resp = client.get_task()
# resp = client.get_timeevent(start_date="2024-01-15")
# resp = client.get_dailycase(start_date="2024-01-15")

# When ready, migrate to the modern API for typed models and more resources:
#
#   from qgendapy import QGendaClient, OData
#   client = QGendaClient()  # credentials from QGENDA_CONF_FILE
#   schedule = client.schedule.list(start_date="2024-01-15")
#   for entry in schedule:
#       print(entry.staff_f_name)
