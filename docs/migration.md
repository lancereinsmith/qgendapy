# Migration Guide

Migrating from the legacy `python-qgenda` library (by JP Jorissen) to `qgendapy`.

## Option 1: Drop-in Replacement (Fastest)

Change one import line and everything else works:

```python
# Before
from qgenda.api.client import QGendaClient

# After
from qgendapy.compat import QGendaClient
```

The compat client accepts the same constructor signature. With `QGENDA_CONF_FILE` set, no arguments are needed:

```python
# Credentials loaded from INI file via QGENDA_CONF_FILE
client = QGendaClient()
client.authenticate()  # still works (no-op -- auth is now automatic)

resp = client.get_schedule(start_date="2024-01-15")
data = resp.json()     # returns list[dict], same as before
```

The response objects mimic `requests.Response` with `.status_code`, `.json()`, `.text`, and `.headers`.

### What's different in compat mode

- `authenticate()` is a no-op -- the modern client auto-authenticates
- `headers` parameter on methods is ignored (httpx manages headers internally)
- `use_caching` and `leader` constructor params are accepted but ignored
- Error handling uses `qgendapy.exceptions.APIError` instead of `qgenda.api.exceptions.HTTPError`

### Your INI config still works

If you use `QGENDA_CONF_FILE` and `QGENDA_CONF_REGION`, those are supported natively. No config changes needed.

## Option 2: Modern Client (Recommended)

The modern client gives you typed models, OData builder, async support, and full API coverage.

### Constructor Changes

```python
# Before
from qgenda.api.client import QGendaClient
client = QGendaClient(
    username="you@hospital.org",
    password="secret",
    company_key="abc",
    api_url="https://api.qgenda.com/",
    api_version="v2",
)
client.authenticate()

# After -- credentials from QGENDA_CONF_FILE
from qgendapy import QGendaClient
client = QGendaClient()
# No authenticate() needed
```

Or with environment variables:

```bash
export QGENDA_EMAIL="you@hospital.org"
export QGENDA_PASSWORD="secret"
export QGENDA_COMPANY_KEY="abc"
```

Or with explicit arguments:

```python
from qgendapy import QGendaClient
client = QGendaClient(
    email="you@hospital.org",       # "username" -> "email"
    password="secret",
    company_key="abc",
    base_url="https://api.qgenda.com/v2",  # combined URL
)
```

### Method Changes

| Legacy | Modern | Notes |
|--------|--------|-------|
| `client.get_schedule(start_date=..., end_date=..., odata_kwargs=...)` | `client.schedule.list(start_date=..., end_date=..., odata=...)` | OData uses builder |
| `client.get_staff(odata_kwargs=...)` | `client.staff.list(odata=...)` | |
| `client.get_facility(odata_kwargs=...)` | `client.facility.list(odata=...)` | |
| `client.get_organization(organization_key=...)` | `client.organization.list(odata=...)` | |
| `client.get_task(odata_kwargs=...)` | `client.task.list(odata=...)` | |
| `client.get_timeevent(start_date=..., odata_kwargs=...)` | `client.time_event.list(start_date=..., odata=...)` | |
| `client.get_dailycase(start_date=..., odata_kwargs=...)` | `client.daily_case.list(start_date=..., odata=...)` | |

### OData Changes

```python
# Before -- raw dict
resp = client.get_staff(odata_kwargs={
    "$select": "FirstName,LastName",
    "$filter": "IsActive eq true",
})

# After -- OData builder (or pass dict to OData.from_kwargs)
from qgendapy import OData

# Option A: Builder
odata = OData().select("FirstName", "LastName").filter("IsActive eq true")
resp = client.staff.list(odata=odata)

# Option B: From legacy dict (minimal changes)
odata = OData.from_kwargs({"$select": "FirstName,LastName", "$filter": "IsActive eq true"})
resp = client.staff.list(odata=odata)
```

### Response Changes

```python
# Before -- requests.Response
resp = client.get_schedule(start_date="2024-01-15")
data = resp.json()  # list[dict]
status = resp.status_code

# After -- QGendaResponse[ScheduleEntry]
resp = client.schedule.list(start_date="2024-01-15")
data = resp.data          # list[dict] -- raw JSON, same as before
status = resp.status_code  # same

# NEW: typed model access
for entry in resp:
    print(entry.task_name)      # attribute access instead of dict["TaskName"]
    print(entry.staff_f_name)   # PascalCase auto-mapped to snake_case
    print(entry._extra)         # any fields not in the model
```

### Error Handling Changes

```python
# Before
from qgenda.api.exceptions import HTTPError, APICallError
try:
    resp = client.get_schedule(start_date="2024-01-15")
except HTTPError:
    ...

# After
from qgendapy.exceptions import APIError, AuthenticationError
try:
    resp = client.schedule.list(start_date="2024-01-15")
except APIError as e:
    print(e.status_code, e.message, e.response_body)
```

## What You Gain

The modern client covers the **entire** QGenda API -- not just the 7 GET endpoints in the legacy library:

- **23 resource groups** with **159 methods** (sync) + **159 methods** (async)
- Full CRUD: create, read, update, delete staff, tasks, facilities, time events, etc.
- Sub-resources: staff tags, skillsets, profiles, pay modifiers, badge IDs, etc.
- Credentialing: 34 methods for contacts, locations, providers, privileges, records, workflows
- Daily operations: configurations, rooms, patient encounters, capacity
- Notification lists, pay codes/rates/pools, staff targets, credit allocations, and more
- **Auto-chunking**: Schedule requests over 100 days are automatically split into batches (the old library silently truncated results)
