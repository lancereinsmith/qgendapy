from unittest.mock import MagicMock

import httpx

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
from qgendapy.odata import OData
from qgendapy.resources.credentialing import CredentialingResource


def _mock_client(response_data, status_code=200):
    client = MagicMock()
    client.company_key = "test-key"
    resp = httpx.Response(
        status_code,
        json=response_data,
        request=httpx.Request("GET", "http://test"),
    )
    client._transport.request.return_value = resp
    return client


class TestContacts:
    def test_returns_contacts(self):
        data = [{"ContactKey": "c1", "FirstName": "Jane", "LastName": "Doe"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.contacts()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CredentialingContact)
        assert resp.items[0].first_name == "Jane"

    def test_odata_support(self):
        client = _mock_client([])
        resource = CredentialingResource(client)
        odata = OData().filter("LastName eq 'Doe'")
        resource.contacts(odata=odata)

        call_args = client._transport.request.call_args
        params = call_args.kwargs.get("params") or call_args[1].get("params", {})
        assert "$filter" in params

    def test_contact_associations(self):
        client = _mock_client([])
        resource = CredentialingResource(client)
        resource.contact_associations("c1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/contacts/c1/associations"

    def test_update_contact_associations(self):
        client = _mock_client({})
        resource = CredentialingResource(client)
        resource.update_contact_associations("c1", data={"LocationKey": "loc1"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/credentialing/contacts/c1/associations"


class TestLocations:
    def test_returns_locations(self):
        data = [{"LocationKey": "loc1", "LocationName": "Hospital A"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.locations()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CredentialingLocation)
        assert resp.items[0].location_name == "Hospital A"

    def test_get_location(self):
        data = {"LocationKey": "loc1", "LocationName": "Hospital A"}
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.get_location("loc1")

        assert len(resp.items) == 1
        assert resp.items[0].location_key == "loc1"

    def test_create_location(self):
        client = _mock_client({"LocationKey": "loc-new"})
        resource = CredentialingResource(client)
        resource.create_location(data={"LocationName": "New Hospital"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/credentialing/location"

    def test_update_location(self):
        client = _mock_client({"LocationKey": "loc1"})
        resource = CredentialingResource(client)
        resource.update_location("loc1", data={"LocationName": "Updated"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"
        assert call_args[0][1] == "/credentialing/location/loc1"

    def test_remove_location_contact(self):
        client = _mock_client("")
        resource = CredentialingResource(client)
        resource.remove_location_contact("c1", "loc1")

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "DELETE"
        assert call_args[0][1] == "/credentialing/location/contacts/c1/location/loc1"


class TestLocationStaff:
    def test_location_staff(self):
        client = _mock_client({})
        resource = CredentialingResource(client)
        resource.location_staff("loc1", "s1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/locations/loc1/staff/s1"

    def test_add_location_staff(self):
        client = _mock_client({})
        resource = CredentialingResource(client)
        resource.add_location_staff("loc1", "s1", data={"Status": "Active"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/credentialing/locations/loc1/staff/s1"

    def test_update_location_staff(self):
        client = _mock_client({})
        resource = CredentialingResource(client)
        resource.update_location_staff("loc1", "s1", data={"Status": "Inactive"})

        call_args = client._transport.request.call_args
        assert call_args[0][0] == "PUT"


class TestProviders:
    def test_returns_providers(self):
        data = [{"StaffKey": "s1", "FirstName": "Dr.", "LastName": "Smith"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.providers()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CredentialingProvider)


class TestPrivileges:
    def test_returns_assigned_privileges(self):
        data = [{"PrivilegeKey": "p1", "PrivilegeName": "Radiology"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.assigned_privileges()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CredentialingPrivilege)


class TestStaffSubResources:
    def test_staff_addresses(self):
        data = [{"AddressKey": "a1", "City": "Chicago", "State": "IL"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.staff_addresses("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], StaffAddress)
        assert resp.items[0].city == "Chicago"

    def test_staff_appointments(self):
        data = [{"AppointmentKey": "ap1", "LocationName": "Hospital A"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.staff_appointments("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], StaffAppointment)

    def test_staff_files(self):
        client = _mock_client([])
        resource = CredentialingResource(client)
        resource.staff_files("s1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/staff/s1/files"

    def test_staff_file(self):
        client = _mock_client({})
        resource = CredentialingResource(client)
        resource.staff_file("s1", params={"fileKey": "f1"})

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/staff/s1/file"

    def test_staff_records(self):
        data = [{"RecordKey": "r1", "RecordName": "License", "Status": "Active"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.staff_records("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CredentialingRecord)

    def test_staff_record_file(self):
        client = _mock_client({})
        resource = CredentialingResource(client)
        resource.staff_record_file("s1", "r1", "f1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/staff/s1/records/r1/files/f1"

    def test_staff_payer_enrollments(self):
        data = [{"EnrollmentKey": "e1", "PayerName": "Aetna", "Status": "Active"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.staff_payer_enrollments("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], PayerEnrollment)

    def test_staff_privileges(self):
        data = [{"PrivilegeKey": "p1"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.staff_privileges("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CredentialingPrivilege)

    def test_staff_professional_accounts(self):
        data = [{"AccountKey": "ac1", "AccountType": "DEA", "AccountNumber": "12345"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.staff_professional_accounts("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], ProfessionalAccount)


class TestWorkflows:
    def test_staff_workflows(self):
        data = [{"WorkflowKey": "w1", "WorkflowName": "Onboarding", "Status": "Active"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.staff_workflows("s1")

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CredentialingWorkflow)

    def test_staff_workflow(self):
        data = {"WorkflowKey": "w1", "WorkflowName": "Onboarding"}
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.staff_workflow("s1", "w1")

        assert len(resp.items) == 1
        assert resp.items[0].workflow_key == "w1"

    def test_staff_workflows_v2(self):
        client = _mock_client([])
        resource = CredentialingResource(client)
        resource.staff_workflows_v2("s1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/staff/s1/workflowsv2"

    def test_global_workflows(self):
        data = [{"WorkflowKey": "w1"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.workflows()

        assert len(resp.items) == 1
        assert isinstance(resp.items[0], CredentialingWorkflow)

    def test_get_workflow(self):
        client = _mock_client({"WorkflowKey": "w1"})
        resource = CredentialingResource(client)
        resource.get_workflow("w1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/workflows/w1"

    def test_workflow_entities(self):
        client = _mock_client([])
        resource = CredentialingResource(client)
        resource.workflow_entities("w1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/workflows/w1/corporateEntities"

    def test_workflow_locations(self):
        client = _mock_client([])
        resource = CredentialingResource(client)
        resource.workflow_locations("w1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/workflows/w1/locations"

    def test_workflow_staff(self):
        client = _mock_client([])
        resource = CredentialingResource(client)
        resource.workflow_staff("w1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/workflows/w1/staff"

    def test_location_workflows(self):
        data = [{"WorkflowKey": "w1"}]
        client = _mock_client(data)
        resource = CredentialingResource(client)
        resp = resource.location_workflows("loc1")

        assert len(resp.items) == 1

    def test_get_location_workflow(self):
        client = _mock_client({"WorkflowKey": "w1"})
        resource = CredentialingResource(client)
        resource.get_location_workflow("loc1", "w1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/locations/loc1/workflows/w1"

    def test_entity_workflows(self):
        client = _mock_client([])
        resource = CredentialingResource(client)
        resource.entity_workflows("ce1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/corporateEntities/ce1/workflows"

    def test_get_entity_workflow(self):
        client = _mock_client({"WorkflowKey": "w1"})
        resource = CredentialingResource(client)
        resource.get_entity_workflow("ce1", "w1")

        call_args = client._transport.request.call_args
        assert call_args[0][1] == "/credentialing/corporateEntities/ce1/workflows/w1"
