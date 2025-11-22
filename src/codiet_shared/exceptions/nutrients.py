from __future__ import annotations
from typing import TYPE_CHECKING, Collection

from ..exceptions.common import CodietException
from ..utils import sig_fig_fmt

if TYPE_CHECKING:
    from ..protocols.nutrients import (
        HasNutrientAttrs,
        NutrientFlag,
        NutrientRatio,
        NutrientRatioMap,
        HasNutrientMasses,
    )


class NutrientError(CodietException):
    """Base Nutrient error."""


class UnknownNutrientError(NutrientError):
    """A nutrient is unknown to the system."""

    def __init__(self, key: str) -> None:
        self.key: str = key

    @property
    def message(self) -> str:
        return f"The nutrient {self.key} is unknown to the system."


class NutrientAliasCollisionError(NutrientError):
    """An alias collides with another nutrient name or alias."""

    def __init__(self, alias: str):
        self.alias = alias

    @property
    def message(self) -> str:
        return f"The alias {self.alias} collides with another nutrient name or alias."


class ExistingNutrientError(NutrientError):
    """The nutrient already exists."""

    def __init__(self, nutrient_name: str):
        self.nutrient_name = nutrient_name

    @property
    def message(self) -> str:
        return f"The nutrient {self.nutrient_name} already exists."


class NutrientAttrError(CodietException):
    """Base class for nutrient attribute errors."""


class NutrientFlagError(NutrientAttrError):
    """Base class for nutrient flag errors."""


class NutrientRatioError(NutrientAttrError):
    """Base class for nutrient ratio errors."""


class UndefinedNutrientRatioError(NutrientRatioError):
    """Raised when the nutrient ratio is not defined on the entity."""

    def __init__(self, *, nutrient_name: str, entity: HasNutrientAttrs) -> None:
        self.nutrient_name = nutrient_name
        self.entity = entity

    @property
    def message(self) -> str:
        return f"{self.nutrient_name} is not defined on this entity."


class DuplicateNutrientRatioError(NutrientRatioError):
    """Raised when the nutrient ratio is already defined on the entity."""

    def __init__(self, *, nutrient_name: str, entity: HasNutrientAttrs) -> None:
        self.nutrient_name = nutrient_name
        self.entity = entity

    @property
    def message(self) -> str:
        return f"{self.nutrient_name} is already defined on this entity."


class UnknownNutrientFlagError(NutrientFlagError):
    """Raised when the nutrient flag is not known to the system."""

    def __init__(self, key: str) -> None:
        self.key = key

    @property
    def message(self) -> str:
        return f"The nutrient flag: {self.key} is not known to the system."


class UndefinedNutrientFlagError(NutrientFlagError):
    """Raised when the nutrient flag is not defined on the entity."""

    def __init__(self, *, flag_name: str, entity: HasNutrientAttrs) -> None:
        self.flag_name = flag_name
        self.has_nutrient_attrs = entity

    @property
    def message(self) -> str:
        return f"The nutrient flag {self.flag_name} is undefined on this entity."


class ExcludedNutrientError(NutrientAttrError):
    """Raised when a non-zero nutrient is excluded by a flag."""

    def __init__(
        self, *, non_zero_nutrient: NutrientRatio, excluding_flag: NutrientFlag
    ):
        self.non_zero_nutrient = non_zero_nutrient
        self.excluding_flag = excluding_flag

    @property
    def message(self) -> str:
        return (
            f"Non-zero nutrient '{self.non_zero_nutrient.nutrient_name}' "
            f"({self.non_zero_nutrient.nutrient_g_per_100g}g per 100g) is excluded by flag "
            f"'{self.excluding_flag.name}' ({self.excluding_flag.value}). "
            f"Nutrient: {self.non_zero_nutrient}, Excluding flag: {self.excluding_flag}"
        )


class FalseFlagWithTrueChildError(NutrientAttrError):
    """Raised when a false flag has a true child flag."""

    def __init__(self, *, false_flag: NutrientFlag, true_child: NutrientFlag) -> None:
        self.false_flag = false_flag
        self.true_child = true_child

    @property
    def message(self) -> str:
        return (
            f"False flag '{self.false_flag.name}' ({self.false_flag.value}) "
            f"has a true child flag '{self.true_child.name}' ({self.true_child.value}). "
            f"This creates an inconsistent state where a parent flag is false "
            f"but its child flag is true. "
            f"False flag: {self.false_flag}, True child: {self.true_child}"
        )


class NonZeroNutrientWithZeroAncError(NutrientAttrError):
    """Raised when a non-zero nutrient has a zero ancestor."""

    def __init__(
        self,
        *,
        nonzero_nutrient: NutrientRatio,
        zero_ancestor: NutrientRatio,
    ) -> None:
        self.nonzero_nutrient = nonzero_nutrient
        self.zero_ancestor = zero_ancestor

    @property
    def message(self) -> str:
        return (
            f"Non-zero nutrient '{self.nonzero_nutrient.nutrient_name}' "
            f"({self.nonzero_nutrient.nutrient_g_per_100g}g per 100g) cannot have a zero ancestor: "
            f"'{self.zero_ancestor.nutrient_name}'. "
            "Either the ancestor must be non-zero or the nutrient must be zero. "
            "Please also adjust any related flags to be consistent with your changes."
        )


class NonZeroParentNutrientWithFullZeroChildrenError(NutrientAttrError):
    """Raised when a non-zero parent nutrient has all children defined as zero."""

    def __init__(
        self,
        *,
        parent_nutrient: NutrientRatio,
        child_nutrients: NutrientRatioMap,
    ) -> None:
        self.parent_nutrient = parent_nutrient
        self.child_nutrients = child_nutrients

    @property
    def message(self) -> str:
        child_names = list(self.child_nutrients.keys())
        return (
            f"Non-zero parent nutrient '{self.parent_nutrient.nutrient_name}' "
            f"({self.parent_nutrient.nutrient_g_per_100g}g per 100g) has all children defined as zero. "
            f"At least one child must be non-zero to sum to the parent's value, or the parent must be zero.\n"
            f"Child nutrients: {child_names}"
        )


class ChildNutrientsExceedParentError(NutrientAttrError):
    """Raised when the sum of child nutrients exceeds the parent nutrient."""

    def __init__(
        self,
        *,
        child_nutrients: NutrientRatioMap,
        parent_nutrient: NutrientRatio,
        ratio: float,
    ) -> None:
        self.child_nutrients = child_nutrients
        self.parent_nutrient = parent_nutrient
        self._ratio = ratio

    @property
    def ratio(self) -> float:
        return self._ratio

    @property
    def message(self) -> str:
        child_names = list(self.child_nutrients.keys())

        child_sum = sum(
            ratio.nutrient_g_per_100g for ratio in self.child_nutrients.values()
        )

        return (
            f"The child nutrients of {self.parent_nutrient.nutrient_name} exceed the stated value for {self.parent_nutrient.nutrient_name}:\n"
            f"{child_sum}g > {self.parent_nutrient.nutrient_g_per_100g}g per 100g.\n"
            f"Child nutrients: {child_names}\n"
            "Either parent must be increased or child nutrient(s) must be reduced."
        )


class ParentNutrientExceedsChildSumError(NutrientAttrError):
    """Raised when the parent nutrient exceeds the sum of its child nutrients."""

    def __init__(
        self,
        *,
        parent_nutrient: NutrientRatio,
        child_nutrients: NutrientRatioMap,
        ratio: float = 1.0,
    ) -> None:
        self.parent_nutrient = parent_nutrient
        self.child_nutrients = child_nutrients
        self._ratio = ratio

    @property
    def message(self) -> str:
        child_names = list(self.child_nutrients.keys())

        child_sum = sum(
            ratio.nutrient_g_per_100g for ratio in self.child_nutrients.values()
        )

        return (
            f"Parent nutrient '{self.parent_nutrient.nutrient_name}' exceeds sum of its child nutrients:\n"
            f"{self.parent_nutrient.nutrient_g_per_100g}g per 100g > {child_sum}g per 100g.\n"
            "Child Nutrients:\n"
            f"{child_names}\n"
            "Either parent must be reduced or child nutrient(s) must be increased."
        )

    @property
    def ratio(self) -> float:
        return self._ratio


class NutrientRatiosExceedOneError(NutrientAttrError):
    """Raised when the total of nutrient ratios exceeds 1.0."""

    def __init__(
        self, *, total: float, nutrient_ratios: Collection[NutrientRatio]
    ) -> None:
        self.total = total
        self.nutrient_ratios = nutrient_ratios

    @property
    def message(self) -> str:
        nutrient_names = [ratio.nutrient_name for ratio in self.nutrient_ratios]
        nutrient_percs = {
            ratio.nutrient_name: sig_fig_fmt(ratio.nutrient_perc)
            for ratio in self.nutrient_ratios
        }
        return (
            f"Total nutrient ratios ({sig_fig_fmt(self.total)}) exceed 1.0. "
            f"Involved nutrients: {nutrient_names}. "
            f"Individual percentages: {nutrient_percs}"
        )

    @property
    def ratio(self) -> float:
        return self.total


class NutrientMassError(CodietException):
    """Base class for nutrient mass errors."""


class UndefinedNutrientMassError(NutrientMassError):
    """Raised when the nutrient mass is not defined on the entity."""

    def __init__(
        self, *, nutrient_name: str, has_nutrient_masses: HasNutrientMasses
    ) -> None:
        self.nutrient_name = nutrient_name
        self.has_nutrient_masses = has_nutrient_masses

    @property
    def message(self) -> str:
        return f"No mass is defined for {self.nutrient_name} on the entity."


__all__ = [
    "NutrientError",
    "UnknownNutrientError",
    "NutrientAliasCollisionError",
    "ExistingNutrientError",
    "NutrientAttrError",
    "NutrientFlagError",
    "NutrientRatioError",
    "UndefinedNutrientRatioError",
    "DuplicateNutrientRatioError",
    "UnknownNutrientFlagError",
    "UndefinedNutrientFlagError",
    "ExcludedNutrientError",
    "FalseFlagWithTrueChildError",
    "NonZeroNutrientWithZeroAncError",
    "NonZeroParentNutrientWithFullZeroChildrenError",
    "ChildNutrientsExceedParentError",
    "ParentNutrientExceedsChildSumError",
    "NutrientRatiosExceedOneError",
    "NutrientMassError",
    "UndefinedNutrientMassError",
]
