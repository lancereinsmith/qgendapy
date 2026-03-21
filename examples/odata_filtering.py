"""Using OData queries to filter, select, and sort API results."""

from qgendapy import OData, QGendaClient

client = QGendaClient()

# Select specific fields only
odata = OData().select("FirstName", "LastName", "Email")
staff = client.staff.list(odata=odata)
for member in staff:
    print(f"{member.first_name} {member.last_name} <{member.email}>")

# Filter active staff
odata = OData().filter("IsActive eq true")
active_staff = client.staff.list(odata=odata)
print(f"Active staff count: {len(active_staff)}")

# Combine select, filter, and orderby
odata = (
    OData()
    .select("StaffFName", "StaffLName", "TaskName", "StartDate")
    .filter("IsPublished eq true")
    .orderby("StartDate desc")
)
schedule = client.schedule.list(start_date="2024-01-01", end_date="2024-01-31", odata=odata)
for entry in schedule:
    print(f"{entry.start_date}: {entry.staff_f_name} - {entry.task_name}")

# Expand related entities
odata = OData().expand("Tags")
tasks = client.task.list(odata=odata)
for task in tasks:
    print(f"{task.task_name} (extra fields: {task._extra})")

client.close()
