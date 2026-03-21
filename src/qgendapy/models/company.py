from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class Company(BaseModel):
    """A QGenda company."""

    company_key: str = ""
    company_name: str = ""
    abbreviation: str = ""
