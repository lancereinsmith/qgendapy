"""Basic usage of qgendapy -- fetching schedules and staff."""

from qgendapy import QGendaClient

# Credentials are loaded from the INI file pointed to by QGENDA_CONF_FILE.
# See env_config.py for details.
client = QGendaClient()

# --- Schedules ---

schedule = client.schedule.list(start_date="2024-01-15", end_date="2024-01-21")
for entry in schedule:
    print(f"{entry.staff_f_name} {entry.staff_l_name}: {entry.task_name}")

# --- Staff ---

staff = client.staff.list()
for member in staff:
    print(f"{member.first_name} {member.last_name}")

# --- Clean up ---

client.close()
