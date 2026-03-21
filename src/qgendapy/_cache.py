from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class CacheBackend(Protocol):
    """Protocol that cache backends must implement."""

    def get(self, key: str) -> dict | list | None: ...

    def set(self, key: str, value: dict | list, ttl: int = 0) -> None: ...

    def delete(self, key: str) -> None: ...


class NullCache:
    """No-op cache backend (default)."""

    def get(self, key: str) -> None:
        return None

    def set(self, key: str, value: dict | list, ttl: int = 0) -> None:
        pass

    def delete(self, key: str) -> None:
        pass
