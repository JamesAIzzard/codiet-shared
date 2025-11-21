from __future__ import annotations
from typing import Any, NotRequired, TypeGuard, TypedDict
from datetime import date
import numbers

from .dto_predicates import has_only_keys
from .quantity_dtos import is_unit_conversion_dto, UnitConversionDTO
from .cost_dtos import is_cost_ratio_dto, CostRatioDTO
from .nutrient_dtos import (
    is_nutrient_ratio_dto,
    is_nutrient_flag_dto,
    NutrientRatioDTO,
    NutrientFlagDTO,
)
from .calories_dtos import is_calories_ratio_dto, CaloriesRatioDTO


class IngredientDTO(TypedDict):
    uid: int | None
    name: str
    description: str
    last_review_date: str
    standard_unit_name: str
    unit_conversions: list[UnitConversionDTO]
    cost_ratio: CostRatioDTO
    gi: float | None
    nutrient_flags: list[NutrientFlagDTO]
    nutrient_ratios: list[NutrientRatioDTO]
    calories_ratio: NotRequired[CaloriesRatioDTO]
    use_as_recipe: bool


def is_ingredient_dto(obj: Any) -> TypeGuard[IngredientDTO]:
    if not isinstance(obj, dict):
        return False

    required_keys = {
        "uid",
        "name",
        "description",
        "last_review_date",
        "standard_unit_name",
        "unit_conversions",
        "cost_ratio",
        "gi",
        "nutrient_flags",
        "nutrient_ratios",
        "use_as_recipe",
    }
    optional_keys = {"calories_ratio"}
    if not has_only_keys(obj, required_keys, optional_keys):
        return False

    if not isinstance(obj.get("name"), str):
        return False
    if not isinstance(obj.get("description"), str):
        return False
    last_review_date = obj.get("last_review_date")
    if not isinstance(last_review_date, str):
        return False
    try:
        date.fromisoformat(last_review_date)
    except (TypeError, ValueError):
        return False
    if not isinstance(obj.get("standard_unit_name"), str):
        return False

    uc_list = obj.get("unit_conversions")
    if not isinstance(uc_list, list):
        return False
    for uc in uc_list:
        if not is_unit_conversion_dto(uc):
            return False

    if not is_cost_ratio_dto(obj.get("cost_ratio")):
        return False

    gi = obj.get("gi")
    if not (isinstance(gi, numbers.Real) or gi is None):
        return False

    nf_list = obj.get("nutrient_flags")
    if not isinstance(nf_list, list):
        return False
    for nf in nf_list:
        if not is_nutrient_flag_dto(nf):
            return False

    nr_list = obj.get("nutrient_ratios")
    if not isinstance(nr_list, list):
        return False
    for nr in nr_list:
        if not is_nutrient_ratio_dto(nr):
            return False

    if "calories_ratio" in obj:
        calories_ratio_dto = obj["calories_ratio"]
        if not is_calories_ratio_dto(calories_ratio_dto):
            return False

    if not isinstance(obj.get("use_as_recipe"), bool):
        return False

    uid_val = obj.get("uid")
    if not (isinstance(uid_val, int) or uid_val is None):
        return False

    return True


class IngredientQuantityDTO(TypedDict):
    ingredient_name: str
    quantity_unit_name: str
    quantity_value: float


def is_ingredient_quantity_dto(obj: Any) -> TypeGuard[IngredientQuantityDTO]:
    return (
        isinstance(obj, dict)
        and has_only_keys(
            obj,
            ("ingredient_name", "quantity_unit_name", "quantity_value"),
        )
        and isinstance(obj.get("ingredient_name"), str)
        and isinstance(obj.get("quantity_unit_name"), str)
        and isinstance(obj.get("quantity_value"), (int, float))
    )
