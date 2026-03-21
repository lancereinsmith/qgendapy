from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar

from qgendapy.exceptions import APIError

if TYPE_CHECKING:
    import httpx

T = TypeVar("T")


@dataclass
class QGendaResponse(Generic[T]):
    """Wrapper around a QGenda API response."""

    data: list[dict] | dict
    status_code: int
    headers: dict[str, str]
    items: list[T] = field(default_factory=list)

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __bool__(self):
        return self.status_code < 400

    def __getitem__(self, index: int) -> T:
        return self.items[index]

    @classmethod
    def from_httpx(cls, resp: httpx.Response, model: type[T] | None = None) -> QGendaResponse[T]:
        """Build a QGendaResponse from an httpx.Response.

        Raises APIError for 4xx/5xx status codes.
        """
        if resp.status_code >= 400:
            try:
                body = resp.json()
            except (ValueError, TypeError):
                body = resp.text
            raise APIError(
                status_code=resp.status_code,
                message=resp.reason_phrase or "API error",
                response_body=body,
            )

        try:
            data = resp.json()
        except (ValueError, TypeError):
            data = {}

        headers = dict(resp.headers)
        items: list[T] = []

        if model is not None:
            if isinstance(data, list):
                items = [model.from_dict(item) for item in data]  # type: ignore[attr-defined]
            elif isinstance(data, dict):
                items = [model.from_dict(data)]  # type: ignore[attr-defined]

        return cls(data=data, status_code=resp.status_code, headers=headers, items=items)
