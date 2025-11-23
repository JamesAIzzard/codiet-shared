from __future__ import annotations
from typing import Hashable

from .common import CodietException


class RecipeError(CodietException):
    """Base class for all recipe-related exceptions."""


class UnnamedRecipeError(RecipeError):
    """Raised when a recipe has no name."""

    @property
    def message(self) -> str:
        return "The recipe has no name."


class NoRecipeDescriptionError(RecipeError):
    """Raised when a recipe has no description."""

    def __init__(self, *, recipe_name: str):
        self.recipe_name = recipe_name

    @property
    def message(self) -> str:
        return f"The recipe '{self.recipe_name}' has no description."


class NoTypicalServiceSizeError(RecipeError):
    """Raised when a recipe has no typical serving size."""

    def __init__(self, *, recipe_name: str):
        self.recipe_name = recipe_name

    @property
    def message(self) -> str:
        return f"The recipe '{self.recipe_name}' has no typical serving size."


class NoCookingTimeError(RecipeError):
    """Raised when a recipe has no cooking time."""

    def __init__(self, *, recipe_name: str):
        self.recipe_name = recipe_name

    @property
    def message(self) -> str:
        return f"The recipe '{self.recipe_name}' has no cooking time."


class RecipeNotFoundError(RecipeError):
    """Raised when a recipe is not found."""

    def __init__(self, key: Hashable):
        self.key: Hashable = key

    @property
    def message(self) -> str:
        return f"Recipe with key '{self.key}' not found."


class DuplicateRecipeError(RecipeError):
    """Raised on trying to add a duplicate recipe."""

    def __init__(self, recipe_name: str):
        self.recipe_name = recipe_name

    @property
    def message(self) -> str:
        return f"Recipe with key '{self.recipe_name}' already exists."


class NoIngredientQuantitiesError(RecipeError):
    """Indicates that this recipe has no ingredient quantities."""

    def __init__(self, *, recipe_name: str) -> None:
        self.recipe_name = recipe_name

    @property
    def message(self) -> str:
        return f"The recipe '{self.recipe_name}' has no ingredient quantities."


__all__ = [
    "RecipeError",
    "UnnamedRecipeError",
    "NoRecipeDescriptionError",
    "NoTypicalServiceSizeError",
    "NoCookingTimeError",
    "RecipeNotFoundError",
    "DuplicateRecipeError",
    "NoIngredientQuantitiesError",
]
