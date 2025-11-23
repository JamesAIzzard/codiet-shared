from __future__ import annotations
from typing import Protocol, Mapping, runtime_checkable, TYPE_CHECKING

from .quantities import HasStandardUnit, HasUnitConversions
from .nutrients import HasNutrientMasses
from .tags import HasTags
from .cost import HasCost, HasCostRatio
from .calories import HasCalories, HasCaloriesRatio

if TYPE_CHECKING:
    from ..dtos.recipes import RecipeDTO, RecipeQuantityDTO
    from .ingredients import IngredientQuantityMap
    from .quantities import Quantity


@runtime_checkable
class Recipe(
    HasUnitConversions,
    HasStandardUnit,
    HasNutrientMasses,
    HasTags,
    HasCostRatio,
    HasCaloriesRatio,
    Protocol,
):
    @property
    def uid(self) -> int | None: ...

    @property
    def name(self) -> str: ...

    @property
    def use_as_ingredient(self) -> bool: ...

    @property
    def description(self) -> str: ...

    @property
    def last_review_date(self) -> str: ...

    @property
    def instructions(self) -> list[str]: ...

    @property
    def servings(self) -> int: ...

    @property
    def cooking_time(self) -> int: ...

    def __eq__(self, other) -> bool:
        if not isinstance(other, Recipe):
            return NotImplemented
        return hash(self) == hash(other)

    @property
    def preparation_ingredient_quantities(self) -> IngredientQuantityMap: ...

    @property
    def composition_ingredient_quantities(self) -> IngredientQuantityMap: ...

    def to_dto(self) -> RecipeDTO: ...


RecipeMap = Mapping[str, Recipe]


@runtime_checkable
class RecipeQuantity(HasNutrientMasses, HasCost, HasCalories, Protocol):
    @property
    def name(self) -> str:
        return self.recipe.name

    @property
    def recipe(self) -> Recipe: ...

    @property
    def quantity(self) -> Quantity: ...

    @property
    def preparation_ingredient_quantities(self) -> IngredientQuantityMap: ...

    @property
    def composition_ingredient_quantities(self) -> IngredientQuantityMap: ...

    def __hash__(self) -> int:
        return hash((self.recipe.name, self.quantity))

    def to_dto(self) -> RecipeQuantityDTO: ...


RecipeQuantityMap = Mapping[str, RecipeQuantity]

__all__ = [
    "Recipe",
    "RecipeMap",
    "RecipeQuantity",
    "RecipeQuantityMap",
]
