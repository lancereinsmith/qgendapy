from __future__ import annotations

from collections.abc import Sequence


class OData:
    """Builder for OData query parameters.

    Supports method chaining::

        params = OData().select("Name", "Email").filter("IsActive eq true").to_params()

    QGenda's API speaks **OData v4** (Microsoft.AspNet.OData), not the older v2
    dialect. The two are mostly compatible for ``$select``, ``$filter`` equality,
    ``$orderby``, and ``$expand``, but a handful of functions changed names:

    +-------------------+-----------------------------+----------------------------+
    | Operation         | OData v2 (rejected, 400)    | OData v4 (works)           |
    +===================+=============================+============================+
    | Substring search  | ``substringof('X', Name)``  | ``contains(Name, 'X')``    |
    +-------------------+-----------------------------+----------------------------+
    | Starts-with       | ``startswith(Name, 'X')``   | ``startswith(Name, 'X')``  |
    +-------------------+-----------------------------+----------------------------+

    Always prefer the v4 form when writing ``$filter`` expressions for QGenda.
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


def escape_literal(value: str) -> str:
    """Escape a string literal for safe interpolation into an OData ``$filter``.

    OData v4 escapes single quotes inside string literals by doubling them.
    Use this on any value that might contain a quote before substituting it
    into a filter expression — e.g.::

        odata = OData().filter(f"StaffKey eq '{escape_literal(staff_key)}'")
    """
    return value.replace("'", "''")


def merge_expand(
    expand: str | Sequence[str] | None,
    odata: OData | None,
) -> OData | None:
    """Merge an ``expand=`` shortcut into an existing :class:`OData` builder.

    Returns ``odata`` unchanged when ``expand`` is ``None``. When ``expand`` is
    provided, returns a new :class:`OData` that preserves every other param
    from ``odata`` and **concatenates** the new nav properties onto any
    existing ``$expand`` (comma-joined). Use this so callers can pass both
    ``odata=OData().expand("Tags")`` and ``expand="Skillset"`` without
    silently dropping one.
    """
    if expand is None:
        return odata
    expand_str = expand if isinstance(expand, str) else ",".join(expand)
    if odata is None:
        return OData().expand(expand_str)
    merged = OData()
    merged._params = dict(odata.to_params())
    existing = merged._params.get("$expand")
    merged._params["$expand"] = f"{existing},{expand_str}" if existing else expand_str
    return merged
