from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class Organization(BaseModel):
    """An organization."""

    organization_key: str = ""
    organization_name: str = ""
