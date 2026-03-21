from __future__ import annotations

from dataclasses import dataclass

from qgendapy.models.common import BaseModel


@dataclass
class CredentialingContact(BaseModel):
    """A credentialing contact."""

    contact_key: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""


@dataclass
class CredentialingLocation(BaseModel):
    """A credentialing location."""

    location_key: str = ""
    location_name: str = ""


@dataclass
class CredentialingProvider(BaseModel):
    """A credentialing provider."""

    staff_key: str = ""
    first_name: str = ""
    last_name: str = ""


@dataclass
class CredentialingPrivilege(BaseModel):
    """A credentialing privilege."""

    privilege_key: str = ""
    privilege_name: str = ""


@dataclass
class CredentialingRecord(BaseModel):
    """A credentialing record."""

    record_key: str = ""
    record_name: str = ""
    status: str = ""


@dataclass
class CredentialingWorkflow(BaseModel):
    """A credentialing workflow."""

    workflow_key: str = ""
    workflow_name: str = ""
    status: str = ""


@dataclass
class StaffAddress(BaseModel):
    """A staff address."""

    address_key: str = ""
    address_type: str = ""
    street: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""


@dataclass
class StaffAppointment(BaseModel):
    """A staff appointment."""

    appointment_key: str = ""
    location_name: str = ""
    status: str = ""


@dataclass
class PayerEnrollment(BaseModel):
    """A payer enrollment."""

    enrollment_key: str = ""
    payer_name: str = ""
    status: str = ""


@dataclass
class ProfessionalAccount(BaseModel):
    """A professional account."""

    account_key: str = ""
    account_type: str = ""
    account_number: str = ""
