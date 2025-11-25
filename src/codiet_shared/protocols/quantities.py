from __future__ import annotations
from typing import Protocol, runtime_checkable, Mapping, Collection, Optional
from enum import Enum
from math import isclose

from ..exceptions.quantities import UndefinedUnitConversionError
from ..dtos.quantities import QuantityDTO, UnitConversionDTO


class UnitType(Enum):
    MASS = "mass"
    VOLUME = "volume"
    COUNT = "count"


class UnitSystem(Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"
    CUSTOM = "custom"


@runtime_checkable
class Unit(Protocol):
    @property
    def uid(self) -> int: ...

    @property
    def name(self) -> str: ...

    @property
    def unit_type(self) -> UnitType: ...

    @property
    def unit_system(self) -> UnitSystem: ...

    @property
    def singular_abbreviation(self) -> str: ...

    @property
    def plural_abbreviation(self) -> str: ...

    @property
    def aliases(self) -> Collection[str]: ...


type UnitMap = Mapping[int, Unit]


@runtime_checkable
class Quantity(Protocol):
    @property
    def unit(self) -> Unit: ...

    @property
    def value(self) -> float: ...

    @property
    def mass_in_grams(self) -> float: ...

    @property
    def unit_name(self) -> str:
        return self.unit.name

    @property
    def is_zero(self) -> bool:
        return self.value == 0

    @property
    def is_non_zero(self) -> bool:
        return self.value != 0

    def __str__(self) -> str:
        return f"{self.value} {self.unit_name}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.unit, self.value))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        return hash(self) == hash(other)

    def to_dto(self) -> QuantityDTO: ...


@runtime_checkable
class IsQuantified(Protocol):
    @property
    def quantity(self) -> Quantity: ...


@runtime_checkable
class UnitConversion(Protocol):
    @property
    def uid(self) -> Optional[int]: ...

    @property
    def unit_uids(self) -> UnitConversionKey: ...

    def get_ratio(self, *, from_unit_uid: int, to_unit_uid: int) -> float: ...

    @property
    def canonical_rep(
        self,
    ) -> tuple[tuple[int, float], tuple[int, float]]:
        """Returns a canonical representation of the conversion as
        ((unit_uid_1, unit_value_1), (unit_uid_2, unit_value_2))."""
        u1, u2 = sorted(self.unit_uids)
        r = float(self.get_ratio(from_unit_uid=u1, to_unit_uid=u2))
        return (u1, 1.0), (u2, r)

    def to_dto(self) -> UnitConversionDTO: ...

    def __hash__(self) -> int:
        (u1, v1), (u2, v2) = self.canonical_rep
        return hash((u1, float(v1), u2, float(v2)))

    def __eq__(self, other) -> bool:
        if not (hasattr(other, "unit_uids") and hasattr(other, "get_ratio")):
            return NotImplemented
        try:
            (u1, v1), (u2, v2) = self.canonical_rep
            ou1, ou2 = sorted(other.unit_uids)
            oratio = float(other.get_ratio(from_unit_uid=ou1, to_unit_uid=ou2))
            (ou1p, _), (ou2p, ov2) = (ou1, 1.0), (ou2, oratio)
        except Exception:
            return False

        return u1 == ou1p and u2 == ou2p and isclose(v2, ov2)

    def __str__(self) -> str:
        (u1, v1), (u2, v2) = self.canonical_rep
        return f"{v1}{u1} <-> {v2}{u2}"

    def __repr__(self) -> str:
        return self.__str__()


type UnitConversionKey = frozenset[int]
type UnitConversionKeys = Collection[UnitConversionKey]
type UnitConversionMap = Mapping[UnitConversionKey, UnitConversion]


class HasUnitConversions(Protocol):
    @property
    def unit_conversions(self) -> UnitConversionMap: ...

    def unit_conversion_is_defined(self, key: UnitConversionKey) -> bool:
        return key in self.unit_conversions

    def assert_unit_conversion_defined(self, key: UnitConversionKey) -> None:
        if not self.unit_conversion_is_defined(key=key):
            raise UndefinedUnitConversionError(key)

    def get_unit_conversion(self, key: UnitConversionKey) -> UnitConversion:
        self.assert_unit_conversion_defined(key)
        return self.unit_conversions[key]


class HasStandardUnit(Protocol):
    @property
    def standard_unit_name(self) -> str: ...


__all__ = [
    "UnitType",
    "UnitSystem",
    "Unit",
    "UnitMap",
    "Quantity",
    "IsQuantified",
    "UnitConversion",
    "UnitConversionKey",
    "UnitConversionKeys",
    "UnitConversionMap",
    "HasUnitConversions",
    "HasStandardUnit",
]
