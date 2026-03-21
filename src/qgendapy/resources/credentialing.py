from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.credentialing import (
    CredentialingContact,
    CredentialingLocation,
    CredentialingPrivilege,
    CredentialingProvider,
    CredentialingRecord,
    CredentialingWorkflow,
    PayerEnrollment,
    ProfessionalAccount,
    StaffAddress,
    StaffAppointment,
)
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class CredentialingResource(BaseResource):
    """Synchronous credentialing endpoints."""

    # -- Contacts --

    def contacts(self, *, odata: OData | None = None) -> QGendaResponse[CredentialingContact]:
        return self._get("/credentialing/contacts", model=CredentialingContact, odata=odata)

    def contact_associations(
        self, contact_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return self._get(f"/credentialing/contacts/{contact_key}/associations", odata=odata)

    def update_contact_associations(self, contact_key: str, *, data: dict) -> QGendaResponse[dict]:
        return self._put(f"/credentialing/contacts/{contact_key}/associations", json=data)

    # -- Locations --

    def locations(self, *, odata: OData | None = None) -> QGendaResponse[CredentialingLocation]:
        return self._get("/credentialing/locations", model=CredentialingLocation, odata=odata)

    def get_location(
        self, location_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingLocation]:
        return self._get(
            f"/credentialing/location/{location_key}",
            model=CredentialingLocation,
            odata=odata,
        )

    def create_location(self, *, data: dict) -> QGendaResponse[CredentialingLocation]:
        return self._post("/credentialing/location", json=data, model=CredentialingLocation)

    def update_location(
        self, location_key: str, *, data: dict
    ) -> QGendaResponse[CredentialingLocation]:
        return self._put(
            f"/credentialing/location/{location_key}",
            json=data,
            model=CredentialingLocation,
        )

    def remove_location_contact(self, contact_key: str, location_key: str) -> QGendaResponse[dict]:
        return self._delete(
            f"/credentialing/location/contacts/{contact_key}/location/{location_key}"
        )

    # -- Location Staff --

    def location_staff(
        self, location_key: str, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return self._get(f"/credentialing/locations/{location_key}/staff/{staff_key}", odata=odata)

    def add_location_staff(
        self, location_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse[dict]:
        return self._post(f"/credentialing/locations/{location_key}/staff/{staff_key}", json=data)

    def update_location_staff(
        self, location_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse[dict]:
        return self._put(f"/credentialing/locations/{location_key}/staff/{staff_key}", json=data)

    # -- Providers --

    def providers(self, *, odata: OData | None = None) -> QGendaResponse[CredentialingProvider]:
        return self._get(
            "/Credentialing/Locations/Providers",  # QGenda API uses PascalCase for this endpoint
            model=CredentialingProvider,
            odata=odata,
        )

    # -- Privileges --

    def assigned_privileges(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingPrivilege]:
        return self._get(
            "/credentialing/privileges/assigned",
            model=CredentialingPrivilege,
            odata=odata,
        )

    # -- Staff sub-resources --

    def staff_addresses(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[StaffAddress]:
        return self._get(
            f"/credentialing/staff/{staff_key}/addresses",
            model=StaffAddress,
            odata=odata,
        )

    def staff_appointments(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[StaffAppointment]:
        return self._get(
            f"/credentialing/staff/{staff_key}/appointments",
            model=StaffAppointment,
            odata=odata,
        )

    def staff_files(self, staff_key: str, *, odata: OData | None = None) -> QGendaResponse[dict]:
        return self._get(f"/credentialing/staff/{staff_key}/files", odata=odata)

    def staff_file(self, staff_key: str, *, params: dict | None = None) -> QGendaResponse[dict]:
        return self._get(f"/credentialing/staff/{staff_key}/file", params=params)

    def staff_records(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingRecord]:
        return self._get(
            f"/credentialing/staff/{staff_key}/records",
            model=CredentialingRecord,
            odata=odata,
        )

    def staff_record_file(
        self, staff_key: str, record_key: str, file_key: str
    ) -> QGendaResponse[dict]:
        return self._get(f"/credentialing/staff/{staff_key}/records/{record_key}/files/{file_key}")

    def staff_payer_enrollments(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[PayerEnrollment]:
        return self._get(
            f"/credentialing/staff/{staff_key}/payerEnrollments",
            model=PayerEnrollment,
            odata=odata,
        )

    def staff_privileges(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingPrivilege]:
        return self._get(
            f"/credentialing/staff/{staff_key}/privileges",
            model=CredentialingPrivilege,
            odata=odata,
        )

    def staff_professional_accounts(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[ProfessionalAccount]:
        return self._get(
            f"/credentialing/staff/{staff_key}/professionalAccounts",
            model=ProfessionalAccount,
            odata=odata,
        )

    # -- Staff Workflows --

    def staff_workflows(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return self._get(
            f"/credentialing/staff/{staff_key}/workflows",
            model=CredentialingWorkflow,
            odata=odata,
        )

    def staff_workflow(
        self, staff_key: str, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return self._get(
            f"/credentialing/staff/{staff_key}/workflows/{workflow_key}",
            model=CredentialingWorkflow,
            odata=odata,
        )

    def staff_workflows_v2(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return self._get(
            f"/credentialing/staff/{staff_key}/workflowsv2",
            model=CredentialingWorkflow,
            odata=odata,
        )

    # -- Workflows (global) --

    def workflows(self, *, odata: OData | None = None) -> QGendaResponse[CredentialingWorkflow]:
        return self._get("/credentialing/workflows", model=CredentialingWorkflow, odata=odata)

    def get_workflow(
        self, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return self._get(
            f"/credentialing/workflows/{workflow_key}",
            model=CredentialingWorkflow,
            odata=odata,
        )

    def workflow_entities(
        self, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return self._get(f"/credentialing/workflows/{workflow_key}/corporateEntities", odata=odata)

    def workflow_locations(
        self, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return self._get(f"/credentialing/workflows/{workflow_key}/locations", odata=odata)

    def workflow_staff(
        self, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return self._get(f"/credentialing/workflows/{workflow_key}/staff", odata=odata)

    # -- Location Workflows --

    def location_workflows(
        self, location_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return self._get(
            f"/credentialing/locations/{location_key}/workflows",
            model=CredentialingWorkflow,
            odata=odata,
        )

    def get_location_workflow(
        self, location_key: str, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return self._get(
            f"/credentialing/locations/{location_key}/workflows/{workflow_key}",
            model=CredentialingWorkflow,
            odata=odata,
        )

    # -- Corporate Entity Workflows --

    def entity_workflows(
        self, entity_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return self._get(
            f"/credentialing/corporateEntities/{entity_key}/workflows",
            model=CredentialingWorkflow,
            odata=odata,
        )

    def get_entity_workflow(
        self, entity_key: str, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return self._get(
            f"/credentialing/corporateEntities/{entity_key}/workflows/{workflow_key}",
            model=CredentialingWorkflow,
            odata=odata,
        )


class AsyncCredentialingResource(AsyncBaseResource):
    """Asynchronous credentialing endpoints."""

    # -- Contacts --

    async def contacts(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingContact]:
        return await self._get("/credentialing/contacts", model=CredentialingContact, odata=odata)

    async def contact_associations(
        self, contact_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return await self._get(f"/credentialing/contacts/{contact_key}/associations", odata=odata)

    async def update_contact_associations(
        self, contact_key: str, *, data: dict
    ) -> QGendaResponse[dict]:
        return await self._put(f"/credentialing/contacts/{contact_key}/associations", json=data)

    # -- Locations --

    async def locations(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingLocation]:
        return await self._get(
            "/credentialing/locations", model=CredentialingLocation, odata=odata
        )

    async def get_location(
        self, location_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingLocation]:
        return await self._get(
            f"/credentialing/location/{location_key}",
            model=CredentialingLocation,
            odata=odata,
        )

    async def create_location(self, *, data: dict) -> QGendaResponse[CredentialingLocation]:
        return await self._post("/credentialing/location", json=data, model=CredentialingLocation)

    async def update_location(
        self, location_key: str, *, data: dict
    ) -> QGendaResponse[CredentialingLocation]:
        return await self._put(
            f"/credentialing/location/{location_key}",
            json=data,
            model=CredentialingLocation,
        )

    async def remove_location_contact(
        self, contact_key: str, location_key: str
    ) -> QGendaResponse[dict]:
        return await self._delete(
            f"/credentialing/location/contacts/{contact_key}/location/{location_key}"
        )

    # -- Location Staff --

    async def location_staff(
        self, location_key: str, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return await self._get(
            f"/credentialing/locations/{location_key}/staff/{staff_key}", odata=odata
        )

    async def add_location_staff(
        self, location_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse[dict]:
        return await self._post(
            f"/credentialing/locations/{location_key}/staff/{staff_key}", json=data
        )

    async def update_location_staff(
        self, location_key: str, staff_key: str, *, data: dict
    ) -> QGendaResponse[dict]:
        return await self._put(
            f"/credentialing/locations/{location_key}/staff/{staff_key}", json=data
        )

    # -- Providers --

    async def providers(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingProvider]:
        return await self._get(
            "/Credentialing/Locations/Providers",  # QGenda API uses PascalCase for this endpoint
            model=CredentialingProvider,
            odata=odata,
        )

    # -- Privileges --

    async def assigned_privileges(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingPrivilege]:
        return await self._get(
            "/credentialing/privileges/assigned",
            model=CredentialingPrivilege,
            odata=odata,
        )

    # -- Staff sub-resources --

    async def staff_addresses(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[StaffAddress]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/addresses",
            model=StaffAddress,
            odata=odata,
        )

    async def staff_appointments(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[StaffAppointment]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/appointments",
            model=StaffAppointment,
            odata=odata,
        )

    async def staff_files(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return await self._get(f"/credentialing/staff/{staff_key}/files", odata=odata)

    async def staff_file(
        self, staff_key: str, *, params: dict | None = None
    ) -> QGendaResponse[dict]:
        return await self._get(f"/credentialing/staff/{staff_key}/file", params=params)

    async def staff_records(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingRecord]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/records",
            model=CredentialingRecord,
            odata=odata,
        )

    async def staff_record_file(
        self, staff_key: str, record_key: str, file_key: str
    ) -> QGendaResponse[dict]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/records/{record_key}/files/{file_key}"
        )

    async def staff_payer_enrollments(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[PayerEnrollment]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/payerEnrollments",
            model=PayerEnrollment,
            odata=odata,
        )

    async def staff_privileges(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingPrivilege]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/privileges",
            model=CredentialingPrivilege,
            odata=odata,
        )

    async def staff_professional_accounts(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[ProfessionalAccount]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/professionalAccounts",
            model=ProfessionalAccount,
            odata=odata,
        )

    # -- Staff Workflows --

    async def staff_workflows(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/workflows",
            model=CredentialingWorkflow,
            odata=odata,
        )

    async def staff_workflow(
        self, staff_key: str, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/workflows/{workflow_key}",
            model=CredentialingWorkflow,
            odata=odata,
        )

    async def staff_workflows_v2(
        self, staff_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            f"/credentialing/staff/{staff_key}/workflowsv2",
            model=CredentialingWorkflow,
            odata=odata,
        )

    # -- Workflows (global) --

    async def workflows(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            "/credentialing/workflows", model=CredentialingWorkflow, odata=odata
        )

    async def get_workflow(
        self, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            f"/credentialing/workflows/{workflow_key}",
            model=CredentialingWorkflow,
            odata=odata,
        )

    async def workflow_entities(
        self, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return await self._get(
            f"/credentialing/workflows/{workflow_key}/corporateEntities", odata=odata
        )

    async def workflow_locations(
        self, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return await self._get(f"/credentialing/workflows/{workflow_key}/locations", odata=odata)

    async def workflow_staff(
        self, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[dict]:
        return await self._get(f"/credentialing/workflows/{workflow_key}/staff", odata=odata)

    # -- Location Workflows --

    async def location_workflows(
        self, location_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            f"/credentialing/locations/{location_key}/workflows",
            model=CredentialingWorkflow,
            odata=odata,
        )

    async def get_location_workflow(
        self, location_key: str, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            f"/credentialing/locations/{location_key}/workflows/{workflow_key}",
            model=CredentialingWorkflow,
            odata=odata,
        )

    # -- Corporate Entity Workflows --

    async def entity_workflows(
        self, entity_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            f"/credentialing/corporateEntities/{entity_key}/workflows",
            model=CredentialingWorkflow,
            odata=odata,
        )

    async def get_entity_workflow(
        self, entity_key: str, workflow_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[CredentialingWorkflow]:
        return await self._get(
            f"/credentialing/corporateEntities/{entity_key}/workflows/{workflow_key}",
            model=CredentialingWorkflow,
            odata=odata,
        )
