from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class TimeEvent(BaseModel):
    """A time event record."""

    time_event_key: str = ""
    staff_key: str = ""
    staff_f_name: str = ""
    staff_l_name: str = ""
    task_name: str = ""
    task_key: str = ""
    start_date: str = ""
    end_date: str = ""
    hours: float | None = None
    comp_key: str = ""
