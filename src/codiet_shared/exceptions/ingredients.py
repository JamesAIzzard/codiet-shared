from __future__ import annotations

from typing import overload

from .common import CodietException


class IngredientError(CodietException):
    """Base class for all ingredient-related exceptions."""

    def __str__(self) -> str:
        return "An ingredient-related error occurred."


class IngredientDTOError(IngredientError):
    """Indicates that an ingredient DTO is invalid."""

    def __init__(self, dto: dict):
        self.json = dto

    def __str__(self) -> str:
        return f"Invalid ingredient JSON: {self.json}"


class IngredientMissingUIDError(IngredientError):
    """Indicates that an ingredient is missing a UID."""

    def __str__(self) -> str:
        return "Ingredient is missing a UID."


class UnnamedIngredientError(IngredientError):
    """Indicates that an ingredient is missing a name."""

    def __str__(self) -> str:
        return "Ingredient is missing a name."


class NoIngredientDescriptionError(IngredientError):
    """Indicates that an ingredient is missing a description."""

    def __init__(self, ingredient_name: str) -> None:
        self.ingredient_name = ingredient_name

    def __str__(self) -> str:
        return f"Ingredient '{self.ingredient_name}' is missing a description."


class IngredientNotFoundError(IngredientError):
    """Indicates that an ingredient was not found in the repository."""

    @overload
    def __init__(self, *, uid: int) -> None: ...

    @overload
    def __init__(self, *, name: str) -> None: ...

    def __init__(self, *, uid: int | None = None, name: str | None = None) -> None:
        self.uid = uid
        self.name = name

    def __str__(self) -> str:
        if self.uid is not None:
            return f"Ingredient with UID '{self.uid}' not found in repository."
        return f"Ingredient with name '{self.name}' not found in repository."


class DuplicateIngredientError(IngredientError):
    """Indicates that an ingredient with this uid already exists in the repository."""

    def __init__(self, ingredient_name: str) -> None:
        self.ingredient_name = ingredient_name

    def __str__(self) -> str:
        return f"Ingredient with name '{self.ingredient_name}' already exists."


class DuplicateIngredientQuantityError(IngredientError):
    """Indicates that an ingredient quantity for this ingredient already
    exists on this entity."""

    def __init__(self, ingredient_uid: int) -> None:
        self.ingredient_uid = ingredient_uid

    def __str__(self) -> str:
        return (
            f"The ingredient with UID '{self.ingredient_uid}' already has a "
            f"quantity on this entity."
        )


class UndefinedIngredientQuantityError(IngredientError):
    """An ingredient quantity for this ingredient does not exist on this entity."""

    def __init__(self, ingredient_uid: int) -> None:
        self.ingredient_uid = ingredient_uid

    def __str__(self) -> str:
        return (
            f"The ingredient with UID '{self.ingredient_uid}' is not defined "
            f"on this entity."
        )


class UndefinedIngredientUnitConvError(IngredientError):
    """The ingredient does not have a defined unit conversion for the specified unit."""

    def __init__(self, ingredient_uid: int, unit_uid: int) -> None:
        self.ingredient_uid = ingredient_uid
        self.unit_uid = unit_uid

    def __str__(self) -> str:
        return (
            f"The ingredient with UID '{self.ingredient_uid}' does not have a defined "
            f"unit conversion for unit UID '{self.unit_uid}'."
        )


__all__ = [
    "IngredientError",
    "IngredientDTOError",
    "IngredientMissingUIDError",
    "UnnamedIngredientError",
    "NoIngredientDescriptionError",
    "IngredientNotFoundError",
    "DuplicateIngredientError",
    "DuplicateIngredientQuantityError",
    "UndefinedIngredientQuantityError",
    "UndefinedIngredientUnitConvError",
]
