from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from qgendapy.models.common import BaseModel


@dataclass
class TagCategory(BaseModel):
    """A category of tags attached to a related entity.

    Returned (nested) on schedule/openshift/task responses when the caller
    asks for them with ``includes="StaffTags"`` (or ``TaskTags`` /
    ``LocationTags``). The ``tags`` field holds the actual tag dicts:
    ``{"Key": int, "Name": str, "LastModifiedDateUtc": str | None}``.
    """

    category_key: int | None = None
    category_name: str = ""
    tags: list[dict] | None = None


def _parse_tag_categories(value: object) -> list[TagCategory] | None:
    """Parse a nested category list into ``TagCategory`` instances.

    Returns the value unchanged when it is ``None`` or already a list of
    ``TagCategory``; only raw dicts are converted.
    """
    if not isinstance(value, list):
        return None
    parsed: list[TagCategory] = []
    for item in value:
        if isinstance(item, TagCategory):
            parsed.append(item)
        elif isinstance(item, dict):
            parsed.append(TagCategory.from_dict(item))
    return parsed


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
    staff_tags: list[TagCategory] | None = None
    task_tags: list[TagCategory] | None = None
    location_tags: list[TagCategory] | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        instance = super().from_dict(data)
        instance.staff_tags = _parse_tag_categories(instance.staff_tags)
        instance.task_tags = _parse_tag_categories(instance.task_tags)
        instance.location_tags = _parse_tag_categories(instance.location_tags)
        return instance


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
    task_tags: list[TagCategory] | None = None
    location_tags: list[TagCategory] | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        instance = super().from_dict(data)
        instance.task_tags = _parse_tag_categories(instance.task_tags)
        instance.location_tags = _parse_tag_categories(instance.location_tags)
        return instance


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
