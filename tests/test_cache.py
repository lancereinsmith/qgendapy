from qgendapy._cache import CacheBackend, NullCache


class TestNullCache:
    def test_get_returns_none(self):
        cache = NullCache()
        assert cache.get("any_key") is None

    def test_set_does_not_raise(self):
        cache = NullCache()
        cache.set("key", {"data": 1}, ttl=60)  # should not raise

    def test_delete_does_not_raise(self):
        cache = NullCache()
        cache.delete("key")  # should not raise


class TestCacheBackendProtocol:
    def test_null_cache_satisfies_protocol(self):
        assert isinstance(NullCache(), CacheBackend)

    def test_custom_backend_satisfies_protocol(self):
        class MemoryCache:
            def __init__(self):
                self._store = {}

            def get(self, key: str) -> dict | list | None:
                return self._store.get(key)

            def set(self, key: str, value: dict | list, ttl: int = 0) -> None:
                self._store[key] = value

            def delete(self, key: str) -> None:
                self._store.pop(key, None)

        cache = MemoryCache()
        assert isinstance(cache, CacheBackend)

        cache.set("k", [1, 2, 3])
        assert cache.get("k") == [1, 2, 3]
        cache.delete("k")
        assert cache.get("k") is None

    def test_incomplete_class_not_protocol(self):
        class BadCache:
            def get(self, key: str):
                return None

        assert not isinstance(BadCache(), CacheBackend)
