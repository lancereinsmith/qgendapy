# qgendapy

Modern Python client for the QGenda REST API.

## Features

- **Full API coverage** -- 159 methods across 23 resource groups
- **Sync + Async** -- `QGendaClient` and `AsyncQGendaClient` with identical APIs
- **Resource-namespaced** -- `client.schedule.list()`, `client.staff.get(key)`, `client.credentialing.workflows()`
- **Typed models** -- Dataclass responses with automatic PascalCase-to-snake_case mapping
- **OData builder** -- `OData().select("Name").filter("IsActive eq true")`
- **3-tier config** -- Explicit args > environment variables > INI file
- **Drop-in compat** -- Migration module for legacy `python-qgenda` users

## Installation

```bash
pip install qgendapy
```

## Quick Start

```python
from qgendapy import QGendaClient, OData

client = QGendaClient(
    email="you@hospital.org",
    password="your-password",
    company_key="your-company-key",
)

# Get this week's schedule
schedule = client.schedule.list(start_date="2024-01-15", end_date="2024-01-21")
for entry in schedule:
    print(f"{entry.staff_f_name} {entry.staff_l_name}: {entry.task_name}")

# OData filtering
odata = OData().select("FirstName", "LastName").filter("IsActive eq true")
staff = client.staff.list(odata=odata)
```

## Configuration

```bash
# Environment variables
export QGENDA_EMAIL="you@hospital.org"
export QGENDA_PASSWORD="your-password"
export QGENDA_COMPANY_KEY="your-company-key"
```

```python
# Then just:
client = QGendaClient()
```

Legacy `QGENDA_CONF_FILE` INI format is also supported.

## Async

```python
from qgendapy import AsyncQGendaClient

async with AsyncQGendaClient() as client:
    schedule = await client.schedule.list(start_date="2024-01-15")
```

## Migrating from python-qgenda

```python
# Change one import:
# from qgenda.api.client import QGendaClient
from qgendapy.compat import QGendaClient

# Everything else works the same
client = QGendaClient(username="...", password="...", company_key="...")
client.authenticate()
resp = client.get_schedule(start_date="2024-01-15")
data = resp.json()
```

See [docs/migration.md](docs/migration.md) for the full migration guide.

## Resources

| Resource | Attribute | Methods |
|----------|-----------|---------|
| Schedule | `client.schedule` | list, audit_log, open_shifts, rotations |
| Staff | `client.staff` | list, get, create, update, tags, skillsets, profiles, pay_modifiers, ... |
| Task | `client.task` | list, create, update, locations, tags, shifts |
| Facility | `client.facility` | list, get, create, update, delete, staff, tags, tasks, ... |
| Time Event | `client.time_event` | list, create, update, delete |
| Daily Case | `client.daily_case` | list, create, update, delete |
| Request | `client.request` | list, approved |
| Request Limit | `client.request_limit` | CRUD + staff_quotas, task_shifts |
| Daily Ops | `client.daily` | configurations, rooms, patient_encounters, capacity |
| Credentialing | `client.credentialing` | contacts, locations, providers, privileges, records, workflows, ... |
| Notification | `client.notification` | CRUD + contacts |
| User | `client.user` | list, get, non_scheduled |
| + 11 more | | pay, tags, profiles, company, organization, ... |

## Acknowledgments

Inspired by [python-qgenda](https://github.com/jpjorissen/python-qgenda) by [JP Jorissen](https://github.com/jpjorissen).

## License

MIT
