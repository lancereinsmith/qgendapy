from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class Facility(BaseModel):
    """A facility / location."""

    location_key: str = ""
    facility_name: str = ""
    abbrev: str = ""
    address: str = ""
    is_active: bool | None = None
