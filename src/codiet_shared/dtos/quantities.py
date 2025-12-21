from __future__ import annotations
from typing import Any, TypeGuard, TypedDict, Collection
import numbers

from .utils import has_only_keys


class UnitDTO(TypedDict):
    uid: int
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
        required=(
            "name",
            "unit_type",
            "unit_system",
            "singular_abbreviation",
            "plural_abbreviation",
            "aliases",
            "uid",
        ),
        optional=(),
    ):
        return False

    if not isinstance(obj.get("uid"), int):
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

    return True


class UnitConversionDTO(TypedDict):
    uid: int | None
    from_unit_uid: int
    from_unit_value: float
    to_unit_uid: int
    to_unit_value: float


UnitConversionKey = frozenset[int]
UnitConversionsDTO = dict[str, UnitConversionDTO]


def get_conversion_keys_from_uc_dtos(
    conversions: Collection[UnitConversionDTO],
) -> set[UnitConversionKey]:
    return {frozenset((uc["from_unit_uid"], uc["to_unit_uid"])) for uc in conversions}


def is_unit_conversion_dto(obj: Any) -> TypeGuard[UnitConversionDTO]:
    if not isinstance(obj, dict):
        return False

    if not has_only_keys(
        obj,
        ("uid", "from_unit_uid", "from_unit_value", "to_unit_uid", "to_unit_value"),
    ):
        return False

    uid_val = obj.get("uid")
    if not (isinstance(uid_val, int) or uid_val is None):
        return False

    return (
        isinstance(obj["from_unit_uid"], int)
        and isinstance(obj["from_unit_value"], numbers.Real)
        and isinstance(obj["to_unit_uid"], int)
        and isinstance(obj["to_unit_value"], numbers.Real)
    )


class QuantityDTO(TypedDict):
    unit_uid: int
    value: float


def is_quantity_dto(obj: Any) -> TypeGuard[QuantityDTO]:
    if not isinstance(obj, dict):
        return False
    if not has_only_keys(obj, ("unit_uid", "value")):
        return False
    if not isinstance(obj["unit_uid"], int):
        return False
    if not isinstance(obj["value"], (int, float)):
        return False
    return True
