from __future__ import annotations
from typing import Protocol, runtime_checkable, Optional, Collection, Mapping

from pygraph import TreeNode, GraphNode

from ..exceptions.nutrients import (
    UndefinedNutrientFlagError,
    UndefinedNutrientRatioError,
    UndefinedNutrientMassError,
)
from ..protocols.quantities import IsQuantified
from ..dtos.nutrients import NutrientFlagDTO, NutrientRatioDTO, NutrientMassDTO
from ..utils import sig_fig_fmt


@runtime_checkable
class Nutrient(TreeNode, Protocol):
    @property
    def uid(self) -> Optional[int]: ...

    @property
    def calories_per_gram(self) -> float: ...

    @property
    def aliases(self) -> Collection[str]: ...

    def has_alias(self, alias: str) -> bool:
        return alias in self.aliases

    def has_zero_calories(self) -> bool:
        return self.calories_per_gram == 0.0

    def __hash__(self) -> int:
        return hash(
            (
                super().__hash__(),
                self.calories_per_gram,
                frozenset(self.aliases),
            )
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Nutrient):
            return NotImplemented
        return (
            super().__eq__(other)
            and self.calories_per_gram == other.calories_per_gram
            and frozenset(self.aliases) == frozenset(other.aliases)
        )


NutrientMap = Mapping[str, Nutrient]


@runtime_checkable
class NutrientFlagDefinition(GraphNode, Protocol):
    @property
    def uid(self) -> Optional[int]: ...

    @property
    def name(self) -> str: ...

    @property
    def directly_excludes_nutrients(self) -> Collection[str]: ...


NutrientFlagDefinitionMap = Mapping[str, NutrientFlagDefinition]


@runtime_checkable
class NutrientFlag(GraphNode, Protocol):
    @property
    def value(self) -> bool: ...

    @property
    def definition(self) -> NutrientFlagDefinition: ...

    @property
    def is_true(self) -> bool:
        return self.value

    @property
    def is_false(self) -> bool:
        return not self.value

    def __hash__(self):
        return hash((self.name, self.value, self.definition))

    def __eq__(self, other):
        if not isinstance(other, NutrientFlag):
            return NotImplemented
        return hash(self) == hash(other)

    def __str__(self):
        return f"{self.name}={self.value}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dto(self) -> NutrientFlagDTO: ...


NutrientFlagMap = Mapping[str, NutrientFlag]


@runtime_checkable
class NutrientRatio(Protocol):
    @property
    def nutrient(self) -> Nutrient: ...

    @property
    def nutrient_perc(self) -> float: ...

    @property
    def nutrient_g_per_g(self) -> float:
        return sig_fig_fmt(self.nutrient_perc)

    @property
    def nutrient_g_per_100g(self) -> float:
        return sig_fig_fmt(self.nutrient_perc * 100.0)

    @property
    def nutrient_name(self) -> str:
        return self.nutrient.name

    @property
    def is_zero(self) -> bool:
        return self.nutrient_perc == 0.0

    @property
    def is_non_zero(self) -> bool:
        return not self.is_zero

    def __str__(self) -> str:
        return f"{self.nutrient_name}: {self.nutrient_g_per_100g}g per 100g"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.nutrient, self.nutrient_perc))

    def __eq__(self, other) -> bool:
        if not isinstance(other, NutrientRatio):
            return NotImplemented
        return hash(self) == hash(other)

    def to_dto(self) -> NutrientRatioDTO: ...


NutrientRatioMap = Mapping[str, NutrientRatio]


@runtime_checkable
class NutrientAttrs(Protocol):
    @property
    def nutrient_ratios(self) -> NutrientRatioMap: ...

    @property
    def nutrient_flags(self) -> NutrientFlagMap: ...

    def update_nutrient_ratios(self, new_ratios: NutrientRatioMap) -> None: ...
    def update_nutrient_flags(self, new_flags: NutrientFlagMap) -> None: ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NutrientAttrs):
            return False
        return (
            self.nutrient_ratios == other.nutrient_ratios
            and self.nutrient_flags == other.nutrient_flags
        )


class HasNutrientAttrs(Protocol):
    @property
    def nutrient_flags(self) -> NutrientFlagMap: ...

    @property
    def nutrient_ratios(self) -> NutrientRatioMap: ...

    def nutrient_ratio_is_defined(self, nutrient_name: str) -> bool:
        return nutrient_name in self.nutrient_ratios

    def nutrient_flag_is_defined(self, flag_name: str) -> bool:
        return flag_name in self.nutrient_flags

    def assert_nutrient_ratio_defined(self, nutrient_name: str) -> None:
        if not self.nutrient_ratio_is_defined(nutrient_name):
            raise UndefinedNutrientRatioError(nutrient_name=nutrient_name, entity=self)

    def assert_nutrient_flag_defined(self, flag_name: str) -> None:
        if not self.nutrient_flag_is_defined(flag_name):
            raise UndefinedNutrientFlagError(flag_name=flag_name, entity=self)

    def get_nutrient_flag(self, flag_name: str) -> NutrientFlag:
        self.assert_nutrient_flag_defined(flag_name)
        return self.nutrient_flags[flag_name]

    def get_nutrient_ratio(self, nutrient_name: str) -> NutrientRatio:
        self.assert_nutrient_ratio_defined(nutrient_name)
        return self.nutrient_ratios[nutrient_name]


@runtime_checkable
class NutrientMass(IsQuantified, Protocol):
    @property
    def nutrient(self) -> Nutrient: ...
    @property
    def nutrient_name(self) -> str:
        return self.nutrient.name

    def to_dto(self) -> NutrientMassDTO: ...


NutrientMassMap = Mapping[str, NutrientMass]


class HasNutrientMasses(HasNutrientAttrs, IsQuantified, Protocol):
    @property
    def nutrient_masses(self) -> NutrientMassMap: ...

    def nutrient_mass_is_defined(self, nutrient_name: str) -> bool:
        return nutrient_name in self.nutrient_masses

    def assert_nutrient_mass_defined(self, nutrient_name: str) -> None:
        if not self.nutrient_mass_is_defined(nutrient_name):
            raise UndefinedNutrientMassError(
                nutrient_name=nutrient_name, has_nutrient_masses=self
            )

    def get_nutrient_mass(self, nutrient_name: str) -> NutrientMass:
        self.assert_nutrient_mass_defined(nutrient_name)
        return self.nutrient_masses[nutrient_name]
