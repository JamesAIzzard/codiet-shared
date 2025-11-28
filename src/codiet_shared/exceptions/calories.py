from __future__ import annotations
from typing import TYPE_CHECKING

from .common import CodietException

if TYPE_CHECKING:
    from ..protocols.nutrients import NutrientRatioMap


class CaloriesError(CodietException):
    """Base exception for calorie-related errors."""

    def __str__(self) -> str:
        return "An calorie-related error occurred."


class NegativeCaloriesError(CaloriesError):
    """Raised when a negative calorie value is encountered."""

    def __init__(self, *, calories: float):
        self.calories = calories

    def __str__(self) -> str:
        return f"Negative calories value ({self.calories}) encountered."


class IncompleteCaloricNutrientsError(CaloriesError):
    """Raised when caloric nutrient ratios are incomplete or invalid."""

    def __init__(self, *, nutrient_ratios: NutrientRatioMap):
        self.nutrient_ratios = nutrient_ratios

    def __str__(self) -> str:
        return "Incomplete caloric nutrient ratios provided."


__all__ = [
    "CaloriesError",
    "NegativeCaloriesError",
    "IncompleteCaloricNutrientsError",
]
