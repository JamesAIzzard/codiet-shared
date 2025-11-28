from __future__ import annotations
from typing import TypedDict, TypeGuard, Any, Collection, Optional
import numbers

from .utils import has_only_keys
from .quantities import QuantityDTO, is_quantity_dto


class NutrientDTO(TypedDict):
    uid: int
    name: str
    description: str
    category: str
    parent: Optional[str]
    calories_per_gram: float
    aliases: list[str]


def is_nutrient_dto(obj: Any) -> TypeGuard[NutrientDTO]:
    if not isinstance(obj, dict):
        return False

    if not has_only_keys(
        mapping=obj,
        required=(
            "name",
            "description",
            "category",
            "parent",
            "calories_per_gram",
            "aliases",
            "uid",
        ),
        optional=(),
    ):
        return False

    if not isinstance(obj.get("name"), str):
        return False
    if not isinstance(obj.get("description"), str):
        return False
    if not isinstance(obj.get("category"), str):
        return False

    parent_val = obj.get("parent")
    if not (isinstance(parent_val, str) or parent_val is None):
        return False

    if not isinstance(obj.get("calories_per_gram"), numbers.Real):
        return False

    aliases_val = obj.get("aliases")
    if not isinstance(aliases_val, list):
        return False
    if not all(isinstance(a, str) for a in aliases_val):
        return False

    uid_val = obj.get("uid")
    if not (isinstance(uid_val, int) or uid_val is None):
        return False

    return True


class NutrientFlagDTO(TypedDict):
    flag_def_uid: int
    flag_value: bool


def is_nutrient_flag_dto(obj: Any) -> TypeGuard[NutrientFlagDTO]:
    return (
        isinstance(obj, dict)
        and has_only_keys(obj, ("flag_def_uid", "flag_value"))
        and isinstance(obj.get("flag_uid"), int)
        and isinstance(obj.get("flag_value"), bool)
    )


class NutrientFlagDefDTO(TypedDict):
    uid: int
    name: str
    parents: list[str]
    directly_excludes_nutrients: list[str]


def is_nutrient_flag_def_dto(obj: Any) -> TypeGuard[NutrientFlagDefDTO]:
    if not isinstance(obj, dict):
        return False

    if not has_only_keys(
        mapping=obj,
        required=("name", "parents", "directly_excludes_nutrients", "uid"),
        optional=(),
    ):
        return False

    if not isinstance(obj.get("name"), str):
        return False
    if not isinstance(obj.get("parents"), list):
        return False
    if not all(isinstance(p, str) for p in obj.get("parents", [])):
        return False
    if not isinstance(obj.get("directly_excludes_nutrients"), list):
        return False
    if not all(isinstance(n, str) for n in obj.get("directly_excludes_nutrients", [])):
        return False

    uid_val = obj.get("uid")
    if not (isinstance(uid_val, int) or uid_val is None):
        return False

    return True


class NutrientRatioDTO(TypedDict):
    nutrient_uid: int
    nutrient_mass_unit_uid: int
    nutrient_mass_value: float
    host_quantity_unit_uid: int
    host_quantity_value: float


def is_nutrient_ratio_dto(obj: Any) -> TypeGuard[NutrientRatioDTO]:
    return (
        isinstance(obj, dict)
        and has_only_keys(
            obj,
            (
                "nutrient_uid",
                "nutrient_mass_unit_uid",
                "nutrient_mass_value",
                "host_quantity_unit_uid",
                "host_quantity_value",
            ),
        )
        and isinstance(obj.get("nutrient_uid"), int)
        and isinstance(obj.get("nutrient_mass_unit_uid"), int)
        and isinstance(obj.get("nutrient_mass_value"), numbers.Real)
        and isinstance(obj.get("host_quantity_unit_uid"), int)
        and isinstance(obj.get("host_quantity_value"), numbers.Real)
    )


NutrientRatiosDTO = Collection[NutrientRatioDTO]
NutrientFlagsDTO = Collection[NutrientFlagDTO]


class NutrientAttrsDTO(TypedDict):
    nutrient_ratios: NutrientRatiosDTO
    nutrient_flags: NutrientFlagsDTO


class NutrientMassDTO(TypedDict):
    nutrient_uid: int
    quantity: QuantityDTO


def is_nutrient_mass_dto(obj: Any) -> TypeGuard[NutrientMassDTO]:
    if not isinstance(obj, dict):
        return False

    if not has_only_keys(obj, ("nutrient_uid", "quantity")):
        return False

    if not isinstance(obj["nutrient_uid"], int):
        return False

    if not is_quantity_dto(obj["quantity"]):
        return False

    return True
