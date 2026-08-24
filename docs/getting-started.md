# Getting Started

## Installation

```bash
pip install qgendapy
# or with uv
uv add qgendapy
```

Requires Python 3.11+.

## Configuration

qgendapy uses a 3-tier configuration system. Values are resolved in order of priority:

### 1. Explicit Arguments (highest priority)

```python
from qgendapy import QGendaClient

client = QGendaClient(
    email="you@hospital.org",
    password="your-password",
    company_key="your-company-key",
    base_url="https://api.qgenda.com/v2",  # optional, this is the default
)
```

### 2. Environment Variables

```bash
export QGENDA_EMAIL="you@hospital.org"
export QGENDA_PASSWORD="your-password"
export QGENDA_COMPANY_KEY="your-company-key"
export QGENDA_BASE_URL="https://api.qgenda.com/v2"  # optional
```

```python
# No arguments needed -- picks up from environment
client = QGendaClient()
```

### 3. INI Config File (lowest priority)

Point to your config file with the `QGENDA_CONF_FILE` environment variable. This format is compatible with the legacy `python-qgenda` library:

```bash
export QGENDA_CONF_FILE="/path/to/qgenda.conf"
export QGENDA_CONF_REGION="qgenda"  # optional, "qgenda" is the default section
```

```ini
[qgenda]
username = you@hospital.org
password = your-password
company_key = your-company-key
api_url = https://api.qgenda.com/
api_version = v2
```

Note: The INI format uses `username` (not `email`) and splits the URL into `api_url` + `api_version`. qgendapy handles this mapping automatically.

```python
# No arguments needed -- picks up from QGENDA_CONF_FILE
client = QGendaClient()
```

## Timeouts

Every request -- including the login POST -- is bounded by a timeout that defaults to **30 seconds** per phase (connect, read, write, pool). This is deliberately more generous than httpx's own 5-second default, which leaves this API no margin. Latency varies by network path: `/staffmember` answers in about a second from a laptop, but has been observed from a cloud VM taking over 5 seconds just to return response *headers* -- enough to turn every whole-roster pull into a `ReadTimeout`.

```python
# A slow batch job: give it longer
client = QGendaClient(timeout=120.0)

# Per-phase control, using httpx's own Timeout object
import httpx
client = QGendaClient(timeout=httpx.Timeout(10.0, read=180.0))

# No timeout at all -- waits indefinitely
client = QGendaClient(timeout=None)
```

The value applies to both HTTP clients the stack builds: the pooled client used for API calls and the short-lived one used for token refresh.

## Authentication

Authentication is automatic. The client obtains an OAuth token on the first API call and refreshes it transparently before it expires (with a 60-second buffer). No `authenticate()` call needed.

```python
client = QGendaClient()
# First call triggers authentication automatically
schedule = client.schedule.list(start_date="2024-01-15")
```

The sync client is thread-safe -- the token refresh uses a `threading.Lock`. The async client uses `asyncio.Lock`.

## Basic Usage

### Fetching Schedules

```python
from qgendapy import QGendaClient

client = QGendaClient()

# Required: start_date. Optional: end_date, includes, odata
schedule = client.schedule.list(
    start_date="2024-01-15",
    end_date="2024-01-21",
)

# Iterate over typed ScheduleEntry objects
for entry in schedule:
    print(f"{entry.start_date}: {entry.staff_f_name} {entry.staff_l_name} - {entry.task_name}")

# Access raw data
print(schedule.data)        # list[dict] -- raw JSON
print(schedule.status_code) # 200
print(len(schedule))        # number of entries
```

#### Auto-Chunking for Large Date Ranges

The QGenda API returns a maximum of 100 days of schedule data per request. qgendapy handles this automatically -- if you request a range longer than 100 days, it splits the request into batches and merges the results:

```python
# This transparently makes multiple API calls and combines the results
schedule = client.schedule.list(
    start_date="2024-01-01",
    end_date="2024-12-31",  # 366 days -- split into 4 requests
)
```

This also applies to `client.schedule.open_shifts()`.

### Staff Members

```python
# List all staff
staff = client.staff.list()

# Get a specific staff member
member = client.staff.get("staff-key-here")

# Get staff tags
tags = client.staff.tags("staff-key-here")

# Create a staff member
client.staff.create(data={"FirstName": "Jane", "LastName": "Doe", "Email": "jane@hospital.org"})
```

### OData Queries

Use the `OData` builder for filtering, selecting, ordering, and expanding:

```python
from qgendapy import OData

# Select specific fields
odata = OData().select("FirstName", "LastName", "Email")
staff = client.staff.list(odata=odata)

# Filter active staff
odata = OData().filter("IsActive eq true")
active_staff = client.staff.list(odata=odata)

# Combine multiple OData options
odata = (
    OData()
    .select("FirstName", "LastName", "Email")
    .filter("IsActive eq true")
    .orderby("LastName asc")
)
staff = client.staff.list(odata=odata)

# Expand related data (OData $expand)
odata = OData().expand("Tags")
staff = client.staff.list(odata=odata)

# Shortcut: pass expand= directly without building an OData
staff = client.staff.list(expand="Tags")
staff = client.staff.list(expand=["Tags", "Skillset"])
```

#### `includes=` vs OData `$expand`

QGenda exposes **two** related-entity selectors and they aren't
interchangeable. OData `$expand` walks the DTO's nav properties; QGenda's
own `includes=` parameter pulls richer nested categories that survive
non-admin scope on schedule-style endpoints. When both are accepted, use
`includes=` for tag/specialty data attached to schedule rows:

```python
# StaffTags inline — Primary Specialty, Sub Specialty, Staff Type, etc.
resp = client.schedule.list(
    start_date="2026-05-22",
    end_date="2026-05-22",
    includes="StaffTags",
    odata=OData().filter("TaskName eq 'Call 1'"),
)
for entry in resp:
    if entry.staff_tags:
        for cat in entry.staff_tags:
            print(cat.category_name, [t["Name"] for t in (cat.tags or [])])
```

Both `client.staff.list()` and `client.staff.get()` also accept `includes=`
for symmetry; verify supported values per your QGenda deployment.

Note: QGenda's API is **OData v4** (Microsoft.AspNet.OData). Use
`contains(field, 'X')` rather than the v2-only `substringof('X', field)`.

### Write Operations

```python
# Create a time event
client.time_event.create(data={
    "StaffKey": "staff-key",
    "TaskKey": "task-key",
    "StartDate": "2024-01-15T08:00:00",
    "EndDate": "2024-01-15T17:00:00",
})

# Update a task
client.task.update(data={
    "TaskKey": "task-key",
    "TaskName": "Updated Name",
})

# Delete a time event
client.time_event.delete("time-event-key")
```

### Facilities (Locations)

```python
# List facilities
facilities = client.facility.list()

# Get staff at a facility
staff = client.facility.staff("location-key")

# Get tasks at a facility
tasks = client.facility.tasks("location-key")
```

## Async Usage

Every resource method has an async counterpart:

```python
import asyncio
from qgendapy import AsyncQGendaClient, OData

async def main():
    async with AsyncQGendaClient() as client:
        # Same API, just await the calls
        schedule = await client.schedule.list(start_date="2024-01-15")
        staff = await client.staff.list(odata=OData().filter("IsActive eq true"))

        for entry in schedule:
            print(entry.task_name)

asyncio.run(main())
```

## Response Objects

All methods return `QGendaResponse[T]`:

```python
response = client.schedule.list(start_date="2024-01-15")

# Typed model instances
response.items          # list[ScheduleEntry]

# Iteration and length
for entry in response:  # iterates over .items
    print(entry.task_name)
len(response)           # number of items

# Raw data access
response.data           # list[dict] or dict -- raw JSON from API
response.status_code    # HTTP status code
response.headers        # response headers dict

# Boolean check
if response:            # True if status_code < 400
    print("Success")
```

### Model Objects

Response models are dataclasses with automatic PascalCase-to-snake_case field mapping:

```python
entry = response.items[0]
entry.schedule_key      # from API's "ScheduleKey"
entry.staff_f_name      # from API's "StaffFName"
entry.task_name         # from API's "TaskName"
entry._extra            # dict of any fields not mapped to known attributes
```

## Error Handling

```python
from qgendapy.exceptions import QGendaError, APIError, AuthenticationError, ConfigurationError

try:
    schedule = client.schedule.list(start_date="2024-01-15")
except AuthenticationError:
    print("Bad credentials")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
    print(e.response_body)  # raw error response
except QGendaError:
    print("Something else went wrong")
```

## Context Managers

Both clients support context managers for clean resource cleanup:

```python
# Sync
with QGendaClient() as client:
    schedule = client.schedule.list(start_date="2024-01-15")

# Async
async with AsyncQGendaClient() as client:
    schedule = await client.schedule.list(start_date="2024-01-15")
```
