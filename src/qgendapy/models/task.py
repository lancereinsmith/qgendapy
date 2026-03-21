from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class Task(BaseModel):
    """A schedulable task."""

    task_key: str = ""
    task_name: str = ""
    abbrev: str = ""
    is_active: bool | None = None
    start_date: str = ""
    end_date: str = ""
    department: str = ""


@dataclass
class TaskShift(BaseModel):
    """A shift definition within a task."""

    task_shift_key: str = ""
    task_key: str = ""
    shift_name: str = ""
    start_time: str = ""
    end_time: str = ""
