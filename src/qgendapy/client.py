from __future__ import annotations

from qgendapy._auth import AsyncAuth, Auth
from qgendapy._cache import CacheBackend, NullCache
from qgendapy._config import resolve_config
from qgendapy._transport import AsyncTransport, Transport
from qgendapy.resources.company import AsyncCompanyResource, CompanyResource
from qgendapy.resources.credentialing import (
    AsyncCredentialingResource,
    CredentialingResource,
)
from qgendapy.resources.credit import (
    AsyncCreditAllocationResource,
    CreditAllocationResource,
)
from qgendapy.resources.daily import AsyncDailyResource, DailyResource
from qgendapy.resources.daily_case import AsyncDailyCaseResource, DailyCaseResource
from qgendapy.resources.facility import AsyncFacilityResource, FacilityResource
from qgendapy.resources.integration import (
    AsyncIntegrationResource,
    IntegrationResource,
)
from qgendapy.resources.notification import (
    AsyncNotificationResource,
    NotificationResource,
)
from qgendapy.resources.organization import (
    AsyncOrganizationResource,
    OrganizationResource,
)
from qgendapy.resources.pay import (
    AsyncPayCodeResource,
    AsyncPayPoolResource,
    AsyncPayRateResource,
    PayCodeResource,
    PayPoolResource,
    PayRateResource,
)
from qgendapy.resources.profile import AsyncProfileResource, ProfileResource
from qgendapy.resources.request import AsyncRequestResource, RequestResource
from qgendapy.resources.request_limit import (
    AsyncRequestLimitResource,
    RequestLimitResource,
)
from qgendapy.resources.schedule import AsyncScheduleResource, ScheduleResource
from qgendapy.resources.staff import AsyncStaffResource, StaffResource
from qgendapy.resources.staff_target import (
    AsyncStaffTargetResource,
    StaffTargetResource,
)
from qgendapy.resources.support import AsyncSupportResource, SupportResource
from qgendapy.resources.tag import AsyncTagResource, TagResource
from qgendapy.resources.task import AsyncTaskResource, TaskResource
from qgendapy.resources.time_event import AsyncTimeEventResource, TimeEventResource
from qgendapy.resources.user import AsyncUserResource, UserResource


class QGendaClient:
    """Synchronous QGenda API client."""

    def __init__(
        self,
        email: str | None = None,
        password: str | None = None,
        company_key: str | None = None,
        base_url: str | None = None,
        cache: CacheBackend | None = None,
    ) -> None:
        config = resolve_config(
            email=email, password=password, company_key=company_key, base_url=base_url
        )
        self._config = config
        self._cache = cache or NullCache()
        self._auth = Auth(email=config.email, password=config.password, base_url=config.base_url)
        self._transport = Transport(auth=self._auth, base_url=config.base_url)

        # Resources
        self.schedule = ScheduleResource(self)
        self.staff = StaffResource(self)
        self.task = TaskResource(self)
        self.facility = FacilityResource(self)
        self.organization = OrganizationResource(self)
        self.time_event = TimeEventResource(self)
        self.daily_case = DailyCaseResource(self)
        self.request = RequestResource(self)
        self.request_limit = RequestLimitResource(self)
        self.daily = DailyResource(self)
        self.company = CompanyResource(self)
        self.tag = TagResource(self)
        self.profile = ProfileResource(self)
        self.pay_code = PayCodeResource(self)
        self.pay_rate = PayRateResource(self)
        self.pay_pool = PayPoolResource(self)
        self.staff_target = StaffTargetResource(self)
        self.credit = CreditAllocationResource(self)
        self.notification = NotificationResource(self)
        self.user = UserResource(self)
        self.integration = IntegrationResource(self)
        self.support = SupportResource(self)
        self.credentialing = CredentialingResource(self)

    @property
    def company_key(self) -> str:
        return self._config.company_key

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> QGendaClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncQGendaClient:
    """Asynchronous QGenda API client."""

    def __init__(
        self,
        email: str | None = None,
        password: str | None = None,
        company_key: str | None = None,
        base_url: str | None = None,
        cache: CacheBackend | None = None,
    ) -> None:
        config = resolve_config(
            email=email, password=password, company_key=company_key, base_url=base_url
        )
        self._config = config
        self._cache = cache or NullCache()
        self._auth = AsyncAuth(
            email=config.email, password=config.password, base_url=config.base_url
        )
        self._transport = AsyncTransport(auth=self._auth, base_url=config.base_url)

        # Resources
        self.schedule = AsyncScheduleResource(self)
        self.staff = AsyncStaffResource(self)
        self.task = AsyncTaskResource(self)
        self.facility = AsyncFacilityResource(self)
        self.organization = AsyncOrganizationResource(self)
        self.time_event = AsyncTimeEventResource(self)
        self.daily_case = AsyncDailyCaseResource(self)
        self.request = AsyncRequestResource(self)
        self.request_limit = AsyncRequestLimitResource(self)
        self.daily = AsyncDailyResource(self)
        self.company = AsyncCompanyResource(self)
        self.tag = AsyncTagResource(self)
        self.profile = AsyncProfileResource(self)
        self.pay_code = AsyncPayCodeResource(self)
        self.pay_rate = AsyncPayRateResource(self)
        self.pay_pool = AsyncPayPoolResource(self)
        self.staff_target = AsyncStaffTargetResource(self)
        self.credit = AsyncCreditAllocationResource(self)
        self.notification = AsyncNotificationResource(self)
        self.user = AsyncUserResource(self)
        self.integration = AsyncIntegrationResource(self)
        self.support = AsyncSupportResource(self)
        self.credentialing = AsyncCredentialingResource(self)

    @property
    def company_key(self) -> str:
        return self._config.company_key

    async def close(self) -> None:
        await self._transport.close()

    async def __aenter__(self) -> AsyncQGendaClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
