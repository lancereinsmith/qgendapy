"""Creating, updating, and deleting resources."""

from qgendapy import QGendaClient

client = QGendaClient()

# --- Create a time event ---

new_event = client.time_event.create(
    data={
        "StaffKey": "abc-123",
        "Date": "2024-02-01",
        "StartTime": "08:00",
        "EndTime": "17:00",
        "TaskKey": "task-456",
    }
)
print(f"Created time event: {new_event.items[0].time_event_key}")

# --- Update a staff member ---

updated = client.staff.update(
    "staff-key-123",
    data={
        "FirstName": "Jane",
        "LastName": "Smith",
        "Email": "jane.smith@hospital.org",
    },
)
print(f"Updated: {updated.items[0].first_name} {updated.items[0].last_name}")

# --- Manage staff tags ---

tags = client.staff.tags("staff-key-123")
for tag in tags:
    print(f"Tag: {tag.tag_name}")

client.staff.add_tag("staff-key-123", data={"TagKey": "tag-789"})

# --- Delete a time event ---

client.time_event.delete("event-key-456")
print("Time event deleted")

client.close()
