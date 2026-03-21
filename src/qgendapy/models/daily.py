from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class DailyCase(BaseModel):
    """A daily case record."""

    daily_case_key: str = ""
    staff_key: str = ""
    staff_f_name: str = ""
    staff_l_name: str = ""
    task_name: str = ""
    task_key: str = ""
    start_date: str = ""
    end_date: str = ""
    case_count: int | None = None
    location_name: str = ""


@dataclass
class DailyConfiguration(BaseModel):
    """A daily configuration."""

    daily_configuration_key: str = ""
    name: str = ""
    description: str = ""
    is_active: bool | None = None


@dataclass
class Room(BaseModel):
    """A daily room."""

    room_key: str = ""
    room_name: str = ""
    location_key: str = ""
    location_name: str = ""


@dataclass
class PatientEncounter(BaseModel):
    """A patient encounter."""

    patient_encounter_key: str = ""
    daily_configuration_key: str = ""
    start_date: str = ""
    end_date: str = ""
    staff_key: str = ""
    room_key: str = ""


@dataclass
class CapacityRoomAssignment(BaseModel):
    """A capacity room assignment."""

    capacity_room_assignment_key: str = ""
    room_key: str = ""
    staff_key: str = ""
    start_date: str = ""
    end_date: str = ""
