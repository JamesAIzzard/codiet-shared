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

    def __str__(self) -> str:
        return "A nutrient-related error occurred."


class UnknownNutrientError(NutrientError):
    """A nutrient is unknown to the system."""

    def __init__(self, uid: int) -> None:
        self.uid: int = uid

    def __str__(self) -> str:
        return f"The nutrient {self.uid} is unknown to the system."


class NutrientAliasCollisionError(NutrientError):
    """Two nutrients share the same alias/name."""

    def __init__(self, nutrient_uids: tuple[int, int], colliding_name: str):
        self.nutrient_uids = nutrient_uids
        self.colliding_name = colliding_name

    def __str__(self) -> str:
        return (
            f"The alias {self.colliding_name} collides with another nutrient "
            "name or alias."
            f"The colliding nutrients have UIDs: {self.nutrient_uids}."
        )


class NutrientAttrError(NutrientError):
    """Base class for nutrient attribute errors."""

    def __str__(self) -> str:
        return "A nutrient attribute-related error occurred."


class NutrientFlagError(NutrientAttrError):
    """Base class for nutrient flag errors."""

    def __str__(self) -> str:
        return "A nutrient flag-related error occurred."


class NutrientRatioError(NutrientAttrError):
    """Base class for nutrient ratio errors."""

    def __str__(self) -> str:
        return "A nutrient ratio-related error occurred."


class UndefinedNutrientRatioError(NutrientRatioError):
    """Raised when the nutrient ratio is not defined on the entity."""

    def __init__(self, *, nutrient_uid: int, entity: HasNutrientAttrs) -> None:
        self.nutrient_uid = nutrient_uid
        self.entity = entity

    def __str__(self) -> str:
        return (
            f"A ratio for nutrient with UID {self.nutrient_uid} "
            "is not defined on this entity."
        )


class DuplicateNutrientRatioError(NutrientRatioError):
    """Raised when the nutrient ratio is already defined on the entity."""

    def __init__(self, *, nutrient_uid: int, entity: HasNutrientAttrs) -> None:
        self.nutrient_uid = nutrient_uid
        self.entity = entity

    def __str__(self) -> str:
        return f"{self.nutrient_uid} is already defined on this entity."


class UnknownNutrientFlagError(NutrientFlagError):
    """Raised when the nutrient flag is not known to the system."""

    def __init__(self, flag_def_uid: str) -> None:
        self.flag_def_uid = flag_def_uid

    def __str__(self) -> str:
        return f"The nutrient flag #{self.flag_def_uid} is not known to the system."


class UndefinedNutrientFlagError(NutrientFlagError):
    """Raised when the nutrient flag is not defined on the entity."""

    def __init__(self, *, flag_def_uid: int, entity: HasNutrientAttrs) -> None:
        self.flag_def_uid = flag_def_uid
        self.has_nutrient_attrs = entity

    def __str__(self) -> str:
        return (
            f"A nutrient flag with definition #{self.flag_def_uid} is not "
            f"defined on this entity."
        )


class ExcludedNutrientError(NutrientAttrError):
    """Raised when a non-zero nutrient is excluded by a flag."""

    def __init__(
        self, *, non_zero_nutrient: NutrientRatio, excluding_flag: NutrientFlag
    ):
        self.non_zero_nutrient = non_zero_nutrient
        self.excluding_flag = excluding_flag

    def __str__(self) -> str:
        return (
            f"The nutrient: {self.non_zero_nutrient.nutrient.name} is non-zero "
            f"and excluded by the true flag {self.excluding_flag.definition.name}."
        )


class FalseFlagWithTrueChildError(NutrientAttrError):
    """Raised when a false flag has a true child flag."""

    def __init__(self, *, false_flag: NutrientFlag, true_child: NutrientFlag) -> None:
        self.false_flag = false_flag
        self.true_child = true_child

    def __str__(self) -> str:
        return (
            f"False flag '{self.false_flag.name}' ({self.false_flag.value}) "
            f"has a true child flag '{self.true_child.name}' ({self.true_child.value})."
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

    def __str__(self) -> str:
        return (
            f"Non-zero nutrient {self.nonzero_nutrient.nutrient_name} has a zero "
            f"ancestor {self.zero_ancestor.nutrient_name}."
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

    def __str__(self) -> str:
        return (
            f"Non-zero parent nutrient {self.parent_nutrient.nutrient_name}"
            "has all children defined as zero. "
            f"At least one child must be non-zero to sum to the parent's value, "
            "or the parent must be zero."
        )


class ChildNutrientsExceedParentError(NutrientAttrError):
    """Raised when the sum of child nutrients exceeds the parent nutrient."""

    def __init__(
        self,
        *,
        child_nutrients: NutrientRatioMap,
        parent_nutrient: NutrientRatio,
    ) -> None:
        self.child_nutrients = child_nutrients
        self.parent_nutrient = parent_nutrient

    def __str__(self) -> str:
        return (
            f"The child nutrients of {self.parent_nutrient.nutrient_name} exceed "
            f"the stated value for {self.parent_nutrient.nutrient_name}."
        )


class ParentNutrientExceedsChildSumError(NutrientAttrError):
    """Raised when the parent nutrient exceeds the sum of its child nutrients."""

    def __init__(
        self,
        *,
        parent_nutrient: NutrientRatio,
        child_nutrients: NutrientRatioMap,
    ) -> None:
        self.parent_nutrient = parent_nutrient
        self.child_nutrients = child_nutrients

    def __str__(self) -> str:
        return (
            f"Parent nutrient {self.parent_nutrient.nutrient_name} exceeds sum of "
            "its child nutrients."
        )


class NutrientRatiosExceedOneError(NutrientAttrError):
    """Raised when the total of nutrient ratios exceeds 1.0."""

    def __init__(
        self, *, total: float, nutrient_ratios: Collection[NutrientRatio]
    ) -> None:
        self.total = total
        self.nutrient_ratios = nutrient_ratios

    def __str__(self) -> str:
        return f"Total nutrient ratios ({sig_fig_fmt(self.total)}) exceed 1.0."


class NutrientMassError(CodietException):
    """Base class for nutrient mass errors."""


class UndefinedNutrientMassError(NutrientMassError):
    """Raised when the nutrient mass is not defined on the entity."""

    def __init__(
        self, *, nutrient_uid: int, has_nutrient_masses: HasNutrientMasses
    ) -> None:
        self.nutrient_uid = nutrient_uid
        self.has_nutrient_masses = has_nutrient_masses

    def __str__(self) -> str:
        return f"No mass is defined for nutrient #{self.nutrient_uid} on the entity."


__all__ = [
    "NutrientError",
    "UnknownNutrientError",
    "NutrientAliasCollisionError",
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
