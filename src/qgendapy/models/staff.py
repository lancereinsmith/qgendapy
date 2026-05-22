from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from qgendapy.models.common import BaseModel


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


@dataclass
class StaffType(BaseModel):
    """A staff type categorical value (e.g., Shareholder, Locum, Staff).

    These are the values shown in QGenda's Settings UI "Staff Type" column.
    Resolve a staff member's ``StaffTypeKey`` to a name with
    ``client.staff_type.list()`` and matching on ``staff_type_key``.
    """

    staff_type_key: str = ""
    staff_type_name: str = ""
    is_active: bool | None = None


@dataclass
class StaffMember(BaseModel):
    """A staff member.

    Mirrors the fields returned by ``GET /staffmember`` against QGenda's
    production API. Anything not declared as a field lands in ``_extra`` —
    if you find a useful field there, please open an issue so we can promote
    it to a typed field.
    """

    staff_key: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    abbrev: str = ""
    npi: str = ""
    is_active: bool | None = None
    start_date: str = ""
    end_date: str = ""
    tags: list[StaffTag] | None = None
    phone: str = ""
    pager: str = ""
    mobile_phone: str = ""
    home_phone: str = ""
    dept_name: str = ""

    # Profile / classification
    primary_profile: str = ""
    primary_profile_key: str = ""
    user_profile: str = ""
    user_profile_key: str = ""
    available_profiles: list[dict] | None = None
    staff_type_key: str = ""
    staff_classification: str = ""
    staff_id: str = ""
    staff_internal_id: str = ""

    # Display / categorical color hooks
    bg_color: str = ""
    text_color: str = ""

    # IDs / org
    comp_key: str = ""
    cal_sync_key: str = ""
    manager: str = ""
    manager_id: str = ""

    # HR / productivity
    fte: float | None = None
    reg_hours: float | None = None
    seniority_date: str = ""
    seniority_value: float | None = None
    daily_unit_average: float | None = None

    # Lifecycle
    last_modified_date_utc: str = ""
    deactivation_date_utc: str = ""
    is_auto_approve_swap: bool | None = None

    # Address
    addr1: str = ""
    addr2: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""

    # External system glue
    bill_sys_id: str = ""
    billing_type_key: str = ""
    emr_id: str = ""
    erp_id: str = ""
    payroll_id: str = ""
    sso_id: str = ""
    ext_call_sys_id: str = ""

    # Carrier metadata
    mobile_service_provider: str = ""
    pager_service_provider: str = ""

    # Free-form contact slots
    other_number1: str = ""
    other_number1_type: str = ""
    other_number2: str = ""
    other_number2_type: str = ""
    other_number3: str = ""
    other_number3_type: str = ""

    # Login activity
    source_of_login: str = ""
    user_last_login_date_time_utc: str = ""

    # Time clock
    time_clock_start_date: str = ""
    time_clock_end_date: str = ""
    time_clock_kiosk_pin: str = ""

    # Payroll
    pay_period_group_name: str = ""
    payroll_start_date: str = ""
    payroll_end_date: str = ""

    # Badges
    badge_ids: list[dict] | None = None
    badges: list[dict] | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        instance = super().from_dict(data)
        if isinstance(instance.tags, list):
            parsed: list[StaffTag] = []
            for item in instance.tags:
                if isinstance(item, StaffTag):
                    parsed.append(item)
                elif isinstance(item, dict):
                    parsed.append(StaffTag.from_dict(item))
            instance.tags = parsed
        return instance
