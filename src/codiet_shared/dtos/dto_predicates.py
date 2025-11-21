from __future__ import annotations
from typing import Any
from collections.abc import Iterable, Mapping


def has_keys(mapping: Mapping[str, Any], required: Iterable[str]) -> bool:
    """Return True if all required keys exist in mapping.

    Keeps DTO presence checks concise and consistent across modules.
    """
    return all(key in mapping for key in required)


def has_type_discriminator(obj: Any, *, field: str = "type") -> bool:
    """Return True if obj is a dict with a string-valued discriminator field.

    The default discriminator key is "type".
    """
    return isinstance(obj, dict) and field in obj and isinstance(obj[field], str)


def has_only_keys(
    mapping: Mapping[str, Any],
    required: Iterable[str],
    optional: Iterable[str] = (),
) -> bool:
    """Return True if mapping contains all required keys and no unexpected ones."""

    required_keys = set(required)
    optional_keys = set(optional)
    present_keys = set(mapping.keys())

    if not required_keys.issubset(present_keys):
        return False

    return present_keys.issubset(required_keys | optional_keys)
