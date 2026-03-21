"""Using the client as a context manager for automatic cleanup."""

from qgendapy import QGendaClient

# The context manager ensures the underlying HTTP connection is closed,
# even if an exception occurs.
with QGendaClient() as client:
    # Schedules
    schedule = client.schedule.list(
        start_date="2024-01-15",
        end_date="2024-01-21",
        includes="Task",
    )
    for entry in schedule:
        print(f"{entry.staff_f_name}: {entry.task_name}")

    # Open shifts
    open_shifts = client.schedule.open_shifts(start_date="2024-01-15")
    print(f"\nOpen shifts: {len(open_shifts)}")

    # Rotations
    rotations = client.schedule.rotations(
        range_start_date="2024-01-01",
        range_end_date="2024-03-31",
    )
    for rotation in rotations:
        print(f"Rotation: {rotation.rotation_name}")
