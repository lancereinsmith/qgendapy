from __future__ import annotations

import re
from dataclasses import dataclass, field, fields


def _pascal_to_snake(name: str) -> str:
    """Convert PascalCase to snake_case."""
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def _build_field_map(cls: type) -> dict[str, str]:
    """Build mapping from PascalCase API keys to snake_case field names."""
    mapping: dict[str, str] = {}
    for f in fields(cls):
        if f.name.startswith("_"):
            continue
        # Convert snake_case field name back to likely PascalCase API key
        pascal = "".join(word.capitalize() for word in f.name.split("_"))
        mapping[pascal] = f.name
        mapping[f.name] = f.name  # also accept snake_case
    return mapping


@dataclass
class BaseModel:
    """Base for all QGenda data models.

    Automatically maps PascalCase API keys to snake_case dataclass fields,
    storing unrecognised keys in ``_extra``.
    """

    _extra: dict = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict) -> BaseModel:
        field_map = _build_field_map(cls)
        known_fields = {f.name for f in fields(cls)}
        kwargs: dict = {}
        extra: dict = {}
        for key, value in data.items():
            snake = _pascal_to_snake(key)
            target = field_map.get(key) or field_map.get(snake)
            if target and target in known_fields and target != "_extra":
                kwargs[target] = value
            else:
                extra[key] = value
        kwargs["_extra"] = extra
        return cls(**kwargs)


@dataclass
class Tag(BaseModel):
    """A QGenda tag."""

    tag_key: str = ""
    tag_name: str = ""
    category_name: str = ""
    is_active: bool | None = None


@dataclass
class Profile(BaseModel):
    """A QGenda profile."""

    profile_key: str = ""
    profile_name: str = ""
    description: str = ""
