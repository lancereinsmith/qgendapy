from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class PayCode(BaseModel):
    """A pay code."""

    pay_code_key: str = ""
    name: str = ""
    code: str = ""
    description: str = ""


@dataclass
class PayRate(BaseModel):
    """A pay rate."""

    pay_rate_key: str = ""
    name: str = ""
    rate: float | None = None
    staff_key: str = ""
    pay_code_key: str = ""


@dataclass
class PayPeriodAmount(BaseModel):
    """A pay pool period amount."""

    pay_period_amount_key: str = ""
    pay_pool_template_key: str = ""
    amount: float | None = None
    period_start_date: str = ""
    period_end_date: str = ""
