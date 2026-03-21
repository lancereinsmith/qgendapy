"""Async client usage with asyncio."""

import asyncio

from qgendapy import AsyncQGendaClient


async def main():
    async with AsyncQGendaClient() as client:
        # Fetch schedule and staff concurrently
        schedule_task = asyncio.create_task(
            client.schedule.list(start_date="2024-01-15", end_date="2024-01-21")
        )
        staff_task = asyncio.create_task(client.staff.list())

        schedule, staff = await asyncio.gather(schedule_task, staff_task)

        print(f"Schedule entries: {len(schedule)}")
        for entry in schedule:
            print(f"  {entry.staff_f_name} {entry.staff_l_name}: {entry.task_name}")

        print(f"\nStaff members: {len(staff)}")
        for member in staff:
            print(f"  {member.first_name} {member.last_name}")


if __name__ == "__main__":
    asyncio.run(main())
