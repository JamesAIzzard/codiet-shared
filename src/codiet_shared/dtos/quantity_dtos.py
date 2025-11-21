from __future__ import annotations
from typing import Any, TypeGuard, TypedDict, Collection
import numbers

from .dto_predicates import has_only_keys


class UnitDTO(TypedDict):
    uid: int | None
    name: str
    unit_type: str
    unit_system: str
    singular_abbreviation: str
    plural_abbreviation: str
    aliases: Collection[str]


def is_unit_dto(obj: Any) -> TypeGuard[UnitDTO]:
    if not isinstance(obj, dict):
        return False

    if not has_only_keys(
        mapping=obj,
        required=("name", "unit_type", "unit_system", "singular_abbreviation", "plural_abbreviation", "aliases", "uid"),
        optional=(),
    ):
        return False

    if not isinstance(obj.get("name"), str):
        return False
    if not isinstance(obj.get("unit_type"), str):
        return False
    if not isinstance(obj.get("unit_system"), str):
        return False
    if not isinstance(obj.get("singular_abbreviation"), str):
        return False
    if not isinstance(obj.get("plural_abbreviation"), str):
        return False

    aliases_val = obj.get("aliases")
    if not isinstance(aliases_val, (list, tuple)):
        return False
    if not all(isinstance(a, str) for a in aliases_val):
        return False

    uid_val = obj.get("uid")
    if not (isinstance(uid_val, int) or uid_val is None):
        return False

    return True


class UnitConversionDTO(TypedDict):
    from_unit_name: str
    from_unit_value: float
    to_unit_name: str
    to_unit_value: float


UnitConversionKey = frozenset[str]
UnitConversionsDTO = dict[str, UnitConversionDTO]


def get_conversion_keys_from_uc_dtos(
    conversions: Collection[UnitConversionDTO],
) -> set[UnitConversionKey]:
    return {frozenset((uc["from_unit_name"], uc["to_unit_name"])) for uc in conversions}


def is_unit_conversion_dto(obj: Any) -> TypeGuard[UnitConversionDTO]:
    if not isinstance(obj, dict):
        return False

    if not has_only_keys(
        obj,
        ("from_unit_name", "from_unit_value", "to_unit_name", "to_unit_value"),
    ):
        return False

    return (
        isinstance(obj["from_unit_name"], str)
        and isinstance(obj["from_unit_value"], numbers.Real)
        and isinstance(obj["to_unit_name"], str)
        and isinstance(obj["to_unit_value"], numbers.Real)
    )


class QuantityDTO(TypedDict):
    unit_name: str
    value: float


def is_quantity_dto(obj: Any) -> TypeGuard[QuantityDTO]:
    if not isinstance(obj, dict):
        return False
    if not has_only_keys(obj, ("unit_name", "value")):
        return False
    if not isinstance(obj["unit_name"], str):
        return False
    if not isinstance(obj["value"], (int, float)):
        return False
    return True
