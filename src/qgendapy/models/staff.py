from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class StaffMember(BaseModel):
    """A staff member."""

    staff_key: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    abbrev: str = ""
    npi: str = ""
    is_active: bool | None = None
    start_date: str = ""
    end_date: str = ""
    tags: list[dict] | None = None
    phone: str = ""
    pager: str = ""
    mobile_phone: str = ""
    dept_name: str = ""


@dataclass
class StaffTag(BaseModel):
    """A tag associated with a staff member."""

    tag_key: str = ""
    tag_name: str = ""
    tag_category_name: str = ""


@dataclass
class StaffSkillset(BaseModel):
    """A skillset (task proficiency) for a staff member."""

    task_key: str = ""
    task_name: str = ""
    level: int | None = None


@dataclass
class StaffProfile(BaseModel):
    """A profile value for a staff member."""

    profile_key: str = ""
    profile_name: str = ""
    value: str = ""


@dataclass
class PayModifier(BaseModel):
    """A pay modifier for a staff member."""

    pay_modifier_key: str = ""
    staff_key: str = ""
    amount: float | None = None
    effective_date: str = ""
