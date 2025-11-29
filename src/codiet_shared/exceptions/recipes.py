from __future__ import annotations
from typing import overload, TYPE_CHECKING

from .common import CodietException

if TYPE_CHECKING:
    from ..protocols.recipes import Recipe


class RecipeError(CodietException):
    """Base class for all recipe-related exceptions."""

    def __str__(self) -> str:
        return "A recipe-related error occurred."


class RecipeMissingUIDError(RecipeError):
    """Raised when a recipe is missing a UID."""

    def __str__(self) -> str:
        return "The recipe is missing a UID."


class UnnamedRecipeError(RecipeError):
    """Raised when a recipe has no name."""

    def __init__(self, recipe: Recipe) -> None:
        self.recipe = recipe

    def __str__(self) -> str:
        return "The recipe has no name."


class NoRecipeDescriptionError(RecipeError):
    """Raised when a recipe has no description."""

    def __init__(self, *, recipe_name: str):
        self.recipe_name = recipe_name

    def __str__(self) -> str:
        return f"The recipe '{self.recipe_name}' has no description."


class NoTypicalServiceSizeError(RecipeError):
    """Raised when a recipe has no typical serving size."""

    def __init__(self, *, recipe_name: str):
        self.recipe_name = recipe_name

    def __str__(self) -> str:
        return f"The recipe '{self.recipe_name}' has no typical serving size."


class NoCookingTimeError(RecipeError):
    """Raised when a recipe has no cooking time."""

    def __init__(self, *, recipe_name: str):
        self.recipe_name = recipe_name

    def __str__(self) -> str:
        return f"The recipe '{self.recipe_name}' has no cooking time."


class RecipeNotFoundError(RecipeError):
    """Raised when a recipe is not found."""

    @overload
    def __init__(self, *, uid: int) -> None: ...

    @overload
    def __init__(self, *, name: str) -> None: ...

    def __init__(self, *, uid: int | None = None, name: str | None = None) -> None:
        self.uid = uid
        self.name = name

    def __str__(self) -> str:
        if self.uid is not None:
            return f"Recipe with UID '{self.uid}' not found."
        return f"Recipe with name '{self.name}' not found."


class DuplicateRecipeError(RecipeError):
    """Raised on trying to add a duplicate recipe."""

    def __init__(self, recipe_name: str):
        self.recipe_name = recipe_name

    def __str__(self) -> str:
        return f"Recipe with key '{self.recipe_name}' already exists."


class NoIngredientQuantitiesError(RecipeError):
    """Indicates that this recipe has no ingredient quantities."""

    def __init__(self, *, recipe_name: str) -> None:
        self.recipe_name = recipe_name

    def __str__(self) -> str:
        return f"The recipe '{self.recipe_name}' has no ingredient quantities."


__all__ = [
    "RecipeError",
    "RecipeMissingUIDError",
    "UnnamedRecipeError",
    "NoRecipeDescriptionError",
    "NoTypicalServiceSizeError",
    "NoCookingTimeError",
    "RecipeNotFoundError",
    "DuplicateRecipeError",
    "NoIngredientQuantitiesError",
]
