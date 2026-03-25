# qgendapy

Modern Python client for the QGenda REST API.

Thank you to JP Jorissen for laying the foundation for this library.

## Features

- **Full API coverage** -- 159 methods across 23 resource groups covering the entire QGenda REST API
- **Sync + Async** -- `QGendaClient` (sync) and `AsyncQGendaClient` (async) with identical APIs
- **Resource-namespaced** -- `client.schedule.list()`, `client.staff.get(key)`, `client.credentialing.workflows()`
- **Typed models** -- Dataclass response models with automatic PascalCase-to-snake_case mapping
- **OData builder** -- Chainable query builder: `OData().select("Name").filter("IsActive eq true")`
- **Auto-chunking** -- Schedule requests over 100 days are automatically split into batches
- **3-tier config** -- Explicit args > environment variables > INI config file
- **Drop-in compat** -- Migration module for legacy `python-qgenda` users
- **httpx-powered** -- Modern HTTP with connection pooling, HTTP/2, and timeouts

## Quick Start

```python
from qgendapy import QGendaClient, OData

# Credentials loaded from INI file pointed to by QGENDA_CONF_FILE env var
client = QGendaClient()

# Get this week's schedule
schedule = client.schedule.list(start_date="2024-01-15", end_date="2024-01-21")
for entry in schedule:
    print(f"{entry.staff_f_name} {entry.staff_l_name}: {entry.task_name}")

# Use OData filtering
odata = OData().select("FirstName", "LastName", "Email").filter("IsActive eq true")
staff = client.staff.list(odata=odata)

# Async usage
from qgendapy import AsyncQGendaClient

async def main():
    async with AsyncQGendaClient() as client:
        schedule = await client.schedule.list(start_date="2024-01-15")
        for entry in schedule:
            print(entry.task_name)
```

## Installation

```bash
pip install qgendapy
# or
uv add qgendapy
```

## Resources

| Resource | Attribute | Endpoints |
|----------|-----------|-----------|
| Schedule | `client.schedule` | list, audit_log, open_shifts, rotations |
| Staff | `client.staff` | list, get, create, update, tags, skillsets, profiles, pay_modifiers, badge_id, ... |
| Task | `client.task` | list, create, update, locations, tags, shifts |
| Facility | `client.facility` | list, get, create, update, delete, staff, tags, tasks, ... |
| Organization | `client.organization` | list |
| Time Event | `client.time_event` | list, create, update, delete |
| Daily Case | `client.daily_case` | list, create, update, delete |
| Request | `client.request` | list, approved |
| Request Limit | `client.request_limit` | list, create, update, delete, staff_quotas, task_shifts |
| Daily Ops | `client.daily` | configurations, rooms, patient_encounters, capacity_room_assignments |
| Company | `client.company` | list |
| Tag | `client.tag` | list |
| Profile | `client.profile` | list |
| Pay Code | `client.pay_code` | list |
| Pay Rate | `client.pay_rate` | list, create, update, delete |
| Pay Pool | `client.pay_pool` | period_amounts |
| Staff Target | `client.staff_target` | list, create, update, delete, locations, staff, task_shifts, profiles |
| Credit | `client.credit` | quotas, update_quota |
| Notification | `client.notification` | list, get, create, update, delete, contacts |
| User | `client.user` | list, get, non_scheduled, non_scheduled_permissions |
| Integration | `client.integration` | upload_file |
| Credentialing | `client.credentialing` | contacts, locations, providers, privileges, staff records, workflows, ... |
| Support | `client.support` | send_message |

## Documentation

- [Getting Started](getting-started.md) -- Installation, configuration, and first API calls
- [Migration Guide](migration.md) -- Migrating from `python-qgenda`
- [API Reference](api/index.md) -- Auto-generated from source code
