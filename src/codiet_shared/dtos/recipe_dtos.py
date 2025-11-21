from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Any, NotRequired, TypeGuard, TypedDict

from .dto_predicates import has_only_keys
from .quantity_dtos import (
    is_unit_conversion_dto,
    UnitConversionDTO,
    QuantityDTO,
    is_quantity_dto
)
from .cost_dtos import is_cost_ratio_dto, CostRatioDTO
from .calories_dtos import is_calories_ratio_dto, CaloriesRatioDTO
from .nutrient_dtos import (
    NutrientFlagDTO,
    NutrientRatioDTO,
    NutrientMassDTO,
    is_nutrient_flag_dto,
    is_nutrient_ratio_dto,
    is_nutrient_mass_dto,
)
from .ingredient_dtos import (
    is_ingredient_quantity_dto,
    IngredientQuantityDTO,
)


@dataclass(frozen=True)
class RecipeIngredientQuantitiesDTO:
    preparation: list[IngredientQuantityDTO]
    composition: list[IngredientQuantityDTO]


class RecipeDTO(TypedDict):
    uid: int | None
    name: str
    use_as_ingredient: bool
    description: str
    last_review_date: str
    servings: int
    cooking_time: int
    instructions: list[str]
    standard_unit_name: str
    preparation_ingredient_quantities: list[IngredientQuantityDTO]
    composition_ingredient_quantities: list[IngredientQuantityDTO]
    unit_conversions: list[UnitConversionDTO]
    tags: list[str]
    quantity: NotRequired[QuantityDTO]
    cost_ratio: NotRequired[CostRatioDTO]
    calories_ratio: NotRequired[CaloriesRatioDTO]
    nutrient_flags: NotRequired[list[NutrientFlagDTO]]
    nutrient_ratios: NotRequired[list[NutrientRatioDTO]]
    nutrient_masses: NotRequired[list[NutrientMassDTO]]


def is_recipe_dto(obj: Any) -> TypeGuard[RecipeDTO]:
    if not isinstance(obj, dict):
        return False

    required_keys = {
        "uid",
        "name",
        "use_as_ingredient",
        "description",
        "last_review_date",
        "instructions",
        "standard_unit_name",
        "preparation_ingredient_quantities",
        "composition_ingredient_quantities",
        "unit_conversions",
        "tags",
        "servings",
        "cooking_time",
    }
    optional_keys = {
        "quantity",
        "cost_ratio",
        "calories_ratio",
        "nutrient_flags",
        "nutrient_ratios",
        "nutrient_masses",
    }
    if not has_only_keys(obj, required_keys, optional_keys):
        return False

    if not isinstance(obj.get("name"), str):
        return False
    if not isinstance(obj.get("use_as_ingredient"), bool):
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

    servings_value = obj.get("servings")
    if not isinstance(servings_value, int):
        return False
    if servings_value <= 0:
        return False

    instr = obj.get("instructions")
    if not isinstance(instr, list):
        return False
    if not all(isinstance(step, str) for step in instr):
        return False

    prep_iq_list = obj.get("preparation_ingredient_quantities")
    if not isinstance(prep_iq_list, list):
        return False
    for iq in prep_iq_list:
        if not is_ingredient_quantity_dto(iq):
            return False

    comp_iq_list = obj.get("composition_ingredient_quantities")
    if not isinstance(comp_iq_list, list):
        return False
    for iq in comp_iq_list:
        if not is_ingredient_quantity_dto(iq):
            return False

    uc_list = obj.get("unit_conversions")
    if not isinstance(uc_list, list):
        return False
    for uc in uc_list:
        if not is_unit_conversion_dto(uc):
            return False

    tags = obj.get("tags")
    if not isinstance(tags, list):
        return False
    if not all(isinstance(tag, str) for tag in tags):
        return False

    cooking_time = obj["cooking_time"]
    if not isinstance(cooking_time, int):
        return False
    if cooking_time <= 0:
        return False

    if "quantity" in obj:
        quantity_dto = obj["quantity"]
        if not is_quantity_dto(quantity_dto):
            return False

    if "cost_ratio" in obj:
        cost_ratio_dto = obj["cost_ratio"]
        if not is_cost_ratio_dto(cost_ratio_dto):
            return False

    if "calories_ratio" in obj:
        calories_ratio_dto = obj["calories_ratio"]
        if not is_calories_ratio_dto(calories_ratio_dto):
            return False

    if "nutrient_flags" in obj:
        nutrient_flags = obj["nutrient_flags"]
        if not isinstance(nutrient_flags, list):
            return False
        for flag_dto in nutrient_flags:
            if not is_nutrient_flag_dto(flag_dto):
                return False

    if "nutrient_ratios" in obj:
        nutrient_ratios = obj["nutrient_ratios"]
        if not isinstance(nutrient_ratios, list):
            return False
        for ratio_dto in nutrient_ratios:
            if not is_nutrient_ratio_dto(ratio_dto):
                return False

    if "nutrient_masses" in obj:
        nutrient_masses = obj["nutrient_masses"]
        if not isinstance(nutrient_masses, list):
            return False
        for mass_dto in nutrient_masses:
            if not is_nutrient_mass_dto(mass_dto):
                return False

    uid_val = obj.get("uid")
    if not (isinstance(uid_val, int) or uid_val is None):
        return False

    return True


class RecipeQuantityDTO(TypedDict):
    recipe_name: str
    quantity_unit_name: str
    quantity_value: float


def is_recipe_quantity_dto(obj: Any) -> TypeGuard[RecipeQuantityDTO]:
    return (
        isinstance(obj, dict)
        and has_only_keys(obj, ("recipe_name", "quantity_unit_name", "quantity_value"))
        and isinstance(obj.get("recipe_name"), str)
        and isinstance(obj.get("quantity_unit_name"), str)
        and isinstance(obj.get("quantity_value"), (int, float))
    )
