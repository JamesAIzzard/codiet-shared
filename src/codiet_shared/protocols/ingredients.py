from __future__ import annotations
from typing import Mapping, Optional, Protocol, runtime_checkable

from ..exceptions.ingredients import UndefinedIngredientQuantityError
from ..dtos.ingredients import IngredientDTO, IngredientQuantityDTO
from .calories import HasCaloriesRatio
from .cost import HasCostRatio, HasCost
from .nutrients import HasNutrientAttrs, HasNutrientMasses
from .quantities import HasUnitConversions


@runtime_checkable
class Ingredient(
    HasUnitConversions, HasNutrientAttrs, HasCostRatio, HasCaloriesRatio, Protocol
):
    @property
    def uid(self) -> Optional[int]: ...

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def last_review_date(self) -> str: ...

    @property
    def standard_unit_name(self) -> str: ...

    @property
    def gi(self) -> Optional[float]: ...

    @property
    def use_as_recipe(self) -> bool: ...

    def to_dto(self) -> IngredientDTO: ...

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                self.description,
                self.standard_unit_name,
                self.gi,
                self.use_as_recipe,
                frozenset((k, hash(v)) for k, v in self.unit_conversions.items()),
                frozenset((k, hash(v)) for k, v in self.nutrient_flags.items()),
                frozenset((k, hash(v)) for k, v in self.nutrient_ratios.items()),
                hash(self.cost_ratio),
                hash(self.calories_ratio),
            )
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Ingredient):
            return NotImplemented
        return hash(self) == hash(other)


IngredientMap = Mapping[str, Ingredient]


@runtime_checkable
class IngredientQuantity(HasNutrientMasses, HasCost, Protocol):
    @property
    def ingredient(self) -> Ingredient: ...

    @property
    def ingredient_name(self) -> str:
        return self.ingredient.name

    def to_dto(self) -> IngredientQuantityDTO: ...

    def __hash__(self) -> int:
        return hash(
            (
                self.ingredient,
                # Ensure mapping is hashable and order-independent
                frozenset((k, hash(v)) for k, v in self.nutrient_masses.items()),
                self.total_cost,
                self.quantity,
            )
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, IngredientQuantity):
            return NotImplemented
        return hash(self) == hash(other)


IngredientQuantityMap = Mapping[int, IngredientQuantity]


class HasIngredientQuantities(Protocol):
    @property
    def ingredient_quantities(self) -> IngredientQuantityMap: ...

    def has_ingredient_quantity(self, ingredient_uid: int) -> bool:
        return ingredient_uid in self.ingredient_quantities

    def assert_has_ingredient_quantity(self, ingredient_uid: int) -> None:
        if not self.has_ingredient_quantity(ingredient_uid):
            raise UndefinedIngredientQuantityError(ingredient_uid=ingredient_uid)

    def get_ingredient_quantity(self, ingredient_uid: int) -> IngredientQuantity:
        self.assert_has_ingredient_quantity(ingredient_uid)
        return self.ingredient_quantities[ingredient_uid]


__all__ = [
    "Ingredient",
    "IngredientMap",
    "IngredientQuantity",
    "IngredientQuantityMap",
    "HasIngredientQuantities",
]