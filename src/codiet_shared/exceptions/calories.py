from __future__ import annotations
from typing import TYPE_CHECKING

from .common import CodietException

if TYPE_CHECKING:
    from ..protocols.nutrients import NutrientRatioMap


class CaloriesError(CodietException):
    """Base class for all calorie-related exceptions."""


class NegativeCaloriesError(CaloriesError):
    def __init__(self, *, calories: float, entity_name: str):
        self.calories = calories
        self.entity_name = entity_name

    @property
    def message(self) -> str:
        return (
            f"Calories cannot be negative: {self.calories} kcal in {self.entity_name}."
        )


class IncompleteCaloricNutrientsError(CaloriesError):
    def __init__(self, *, nutrient_ratios: NutrientRatioMap):
        self.nutrient_ratios = nutrient_ratios

    @property
    def message(self) -> str:
        return (
            f"Mandatory caloric nutrient ratios missing: {self.nutrient_ratios}. "
            "Ensure all required nutrients are provided."
        )


__all__ = [
    "CaloriesError",
    "NegativeCaloriesError",
    "IncompleteCaloricNutrientsError",
]
