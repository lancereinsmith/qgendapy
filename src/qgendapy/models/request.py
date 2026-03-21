from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class Request(BaseModel):
    """A schedule request."""

    request_key: str = ""
    staff_key: str = ""
    start_date: str = ""
    end_date: str = ""
    type: str = ""
    status: str = ""
    notes: str = ""
    task_name: str = ""
    task_key: str = ""
    is_removed: bool | None = None


@dataclass
class ApprovedRequest(BaseModel):
    """An approved schedule request."""

    request_key: str = ""
    staff_key: str = ""
    start_date: str = ""
    end_date: str = ""
    type: str = ""
    status: str = ""
    notes: str = ""
    task_name: str = ""
    task_key: str = ""


@dataclass
class RequestLimit(BaseModel):
    """A request limit configuration."""

    request_limit_key: str = ""
    name: str = ""
    start_date: str = ""
    end_date: str = ""
    limit: int | None = None
    type: str = ""
