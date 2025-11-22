from __future__ import annotations
from typing import Any

from .common import CodietException


class IngredientError(CodietException):
    """Base class for all ingredient-related exceptions."""


class IngredientDTOError(IngredientError):
    """Indicates that an ingredient DTO is invalid."""

    def __init__(self, dto: Any):
        self.json = dto

    @property
    def message(self) -> str:
        return f"Invalid ingredient JSON: {self.json}"


class IngredientNotFoundError(IngredientError):
    """Indicates that an ingredient with this namewas not found in the repository."""

    def __init__(self, ingredient_name: str):
        self.ingredient_name = ingredient_name

    @property
    def message(self) -> str:
        return f"Ingredient '{self.ingredient_name}' not found in repository"


class DuplicateIngredientError(IngredientError):
    """Indicates that an ingredient with this name already exists in the repository."""

    def __init__(self, ingredient_name: str) -> None:
        self.ingredient_name = ingredient_name

    @property
    def message(self) -> str:
        return f"Ingredient '{self.ingredient_name}' already exists."


class DuplicateIngredientQuantityError(IngredientError):
    """Indicates that an ingredient quantity for this ingredient already
    exists on this entity."""

    def __init__(self, ingredient_name: str) -> None:
        self.ingredient_name = ingredient_name

    @property
    def message(self) -> str:
        return f"The ingredient {self.ingredient_name} is duplicated on this entity."


class UndefinedIngredientQuantityError(IngredientError):
    """An ingredient quantity for this ingredient does not exist on this entity."""

    def __init__(self, ingredient_name: str) -> None:
        self.ingredient_name = ingredient_name

    @property
    def message(self) -> str:
        return f"The ingredient {self.ingredient_name} is not defined on this entity."


class UndefinedIngredientUnitConvError(IngredientError):
    """The ingredient does not have a defined unit conversion for the specified unit."""

    def __init__(self, ingredient_name: str, unit_name: str) -> None:
        self.ingredient_name = ingredient_name
        self.unit_name = unit_name

    @property
    def message(self) -> str:
        return (
            f"The ingredient {self.ingredient_name} does not have a defined "
            f"unit conversion for {self.unit_name}."
        )


class NoIngredientQuantitiesError(IngredientError):
    """Indicates that this entity has no ingredient quantities."""

    def __init__(self) -> None:
        pass

    @property
    def message(self) -> str:
        return "This entity has no ingredient quantities."


__all__ = [
    "IngredientError",
    "IngredientDTOError",
    "IngredientNotFoundError",
    "DuplicateIngredientError",
    "DuplicateIngredientQuantityError",
    "UndefinedIngredientQuantityError",
    "UndefinedIngredientUnitConvError",
    "NoIngredientQuantitiesError",
]
