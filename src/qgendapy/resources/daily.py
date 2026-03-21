from __future__ import annotations

from typing import TYPE_CHECKING

from qgendapy.models.daily import (
    CapacityRoomAssignment,
    DailyConfiguration,
    PatientEncounter,
    Room,
)
from qgendapy.resources._base import AsyncBaseResource, BaseResource

if TYPE_CHECKING:
    from qgendapy.odata import OData
    from qgendapy.response import QGendaResponse


class DailyResource(BaseResource):
    """Synchronous daily endpoints."""

    def configurations(self, *, odata: OData | None = None) -> QGendaResponse[DailyConfiguration]:
        return self._get("/daily/dailyconfiguration", model=DailyConfiguration, odata=odata)

    def get_configuration(
        self, daily_configuration_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[DailyConfiguration]:
        return self._get(
            f"/daily/dailyconfiguration/{daily_configuration_key}",
            model=DailyConfiguration,
            odata=odata,
        )

    def rooms(self, *, odata: OData | None = None) -> QGendaResponse[Room]:
        return self._get("/daily/room", model=Room, odata=odata)

    def patient_encounters(
        self,
        *,
        daily_configuration_key: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        includes: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[PatientEncounter]:
        params: dict[str, str] = {}
        if daily_configuration_key:
            params["dailyConfigurationKey"] = daily_configuration_key
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if includes:
            params["includes"] = includes
        return self._get(
            "/daily/patientencounter",
            params=params,
            model=PatientEncounter,
            odata=odata,
        )

    def create_patient_encounter(self, *, data: dict) -> QGendaResponse[PatientEncounter]:
        return self._post("/daily/patientencounter", json=data, model=PatientEncounter)

    def update_patient_encounter(self, *, data: dict) -> QGendaResponse[PatientEncounter]:
        return self._put("/daily/patientencounter", json=data, model=PatientEncounter)

    def delete_patient_encounter(self, patient_encounter_key: str) -> QGendaResponse:
        return self._delete(f"/daily/patientencounter/{patient_encounter_key}")

    def capacity_room_assignments(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[CapacityRoomAssignment]:
        return self._get(
            "/daily/capacityroomassignment",
            model=CapacityRoomAssignment,
            odata=odata,
        )


class AsyncDailyResource(AsyncBaseResource):
    """Asynchronous daily endpoints."""

    async def configurations(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[DailyConfiguration]:
        return await self._get("/daily/dailyconfiguration", model=DailyConfiguration, odata=odata)

    async def get_configuration(
        self, daily_configuration_key: str, *, odata: OData | None = None
    ) -> QGendaResponse[DailyConfiguration]:
        return await self._get(
            f"/daily/dailyconfiguration/{daily_configuration_key}",
            model=DailyConfiguration,
            odata=odata,
        )

    async def rooms(self, *, odata: OData | None = None) -> QGendaResponse[Room]:
        return await self._get("/daily/room", model=Room, odata=odata)

    async def patient_encounters(
        self,
        *,
        daily_configuration_key: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        includes: str | None = None,
        odata: OData | None = None,
    ) -> QGendaResponse[PatientEncounter]:
        params: dict[str, str] = {}
        if daily_configuration_key:
            params["dailyConfigurationKey"] = daily_configuration_key
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if includes:
            params["includes"] = includes
        return await self._get(
            "/daily/patientencounter",
            params=params,
            model=PatientEncounter,
            odata=odata,
        )

    async def create_patient_encounter(self, *, data: dict) -> QGendaResponse[PatientEncounter]:
        return await self._post("/daily/patientencounter", json=data, model=PatientEncounter)

    async def update_patient_encounter(self, *, data: dict) -> QGendaResponse[PatientEncounter]:
        return await self._put("/daily/patientencounter", json=data, model=PatientEncounter)

    async def delete_patient_encounter(self, patient_encounter_key: str) -> QGendaResponse:
        return await self._delete(f"/daily/patientencounter/{patient_encounter_key}")

    async def capacity_room_assignments(
        self, *, odata: OData | None = None
    ) -> QGendaResponse[CapacityRoomAssignment]:
        return await self._get(
            "/daily/capacityroomassignment",
            model=CapacityRoomAssignment,
            odata=odata,
        )
