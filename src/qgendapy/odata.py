from __future__ import annotations


class OData:
    """Builder for OData query parameters.

    Supports method chaining::

        params = OData().select("Name", "Email").filter("IsActive eq true").to_params()
    """

    def __init__(self) -> None:
        self._params: dict[str, str] = {}

    def select(self, *fields: str) -> OData:
        """Set the $select parameter."""
        self._params["$select"] = ",".join(fields)
        return self

    def filter(self, expr: str) -> OData:
        """Set the $filter parameter."""
        self._params["$filter"] = expr
        return self

    def orderby(self, expr: str) -> OData:
        """Set the $orderby parameter."""
        self._params["$orderby"] = expr
        return self

    def expand(self, expr: str) -> OData:
        """Set the $expand parameter."""
        self._params["$expand"] = expr
        return self

    def to_params(self) -> dict[str, str]:
        """Return a copy of the accumulated parameters."""
        return dict(self._params)

    @classmethod
    def from_kwargs(cls, kwargs: dict[str, str]) -> OData:
        """Create from a dict whose keys start with ``$``."""
        odata = cls()
        odata._params = {k: v for k, v in kwargs.items() if k.startswith("$")}
        return odata
