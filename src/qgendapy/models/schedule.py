from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class ScheduleEntry(BaseModel):
    """A single schedule entry."""

    schedule_key: str = ""
    start_date: str = ""
    end_date: str = ""
    staff_key: str = ""
    staff_f_name: str = ""
    staff_l_name: str = ""
    staff_abbrev: str = ""
    task_name: str = ""
    task_key: str = ""
    task_abbrev: str = ""
    comp_name: str = ""
    comp_key: str = ""
    location_name: str = ""
    location_key: str = ""
    notes: str = ""
    credit: float | None = None
    is_published: bool | None = None
    is_locked: bool | None = None
    is_struck: bool | None = None


@dataclass
class AuditLogEntry(BaseModel):
    """A schedule audit log entry."""

    schedule_key: str = ""
    modified_date: str = ""
    modified_by: str = ""
    action: str = ""
    field_name: str = ""
    old_value: str = ""
    new_value: str = ""


@dataclass
class OpenShift(BaseModel):
    """An open (unfilled) shift."""

    schedule_key: str = ""
    start_date: str = ""
    end_date: str = ""
    task_name: str = ""
    task_key: str = ""
    location_name: str = ""
    location_key: str = ""


@dataclass
class Rotation(BaseModel):
    """A rotation assignment."""

    rotation_key: str = ""
    rotation_name: str = ""
    start_date: str = ""
    end_date: str = ""
    staff_key: str = ""
    staff_f_name: str = ""
    staff_l_name: str = ""
    task_name: str = ""
    task_key: str = ""
