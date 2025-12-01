"""
Many of the other domain entities exclusively use UID to identify instances.
Unit conversions are a more interesting case, because they are stored as singleton
instances independently (for the constant conversions - e.g., gram to kilogram)
but are also associated with entities (e.g., an ingredient has a unit conversion
for cup to gram). Therefore, we always use key-based identification for
unit conversions.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, overload

from ..exceptions.common import CodietException

if TYPE_CHECKING:
    from ..protocols.quantities import UnitConversionKey


class UnitError(CodietException):
    """Base Unit error."""

    def __str__(self) -> str:
        return "A unit-related error occurred."


class UnknownUnitError(UnitError):
    """A unit is unknown to the system."""

    @overload
    def __init__(self, *, uid: int) -> None: ...

    @overload
    def __init__(self, *, name: str) -> None: ...

    def __init__(self, *, uid: int | None = None, name: str | None = None) -> None:
        self.uid = uid
        self.name = name

    def __str__(self) -> str:
        if self.uid is not None:
            return f"The unit #{self.uid} is unknown to the system."
        return f"The unit '{self.name}' is unknown to the system."


class QuantityError(CodietException):
    """General base class for quantity errors."""

    def __str__(self) -> str:
        return "A quantity-related error occurred."


class NegativeQuantityError(QuantityError):
    """Raised when a quantity is negative."""

    def __init__(self, quantity: float):
        self.quantity = quantity

    def __str__(self) -> str:
        return f"The quantity is negative: {self.quantity}."


class ZeroQuantityError(QuantityError):
    """Raised when a quantity is zero."""

    def __str__(self) -> str:
        return "The quantity is zero."


class UnitConversionError(CodietException):
    """Base class for unit conversion errors."""

    def __str__(self) -> str:
        return "A unit conversion-related error occurred."


class UnitConversionNotFoundError(UnitConversionError):
    """Raised when a unit conversion is not found."""

    def __init__(self, key: UnitConversionKey) -> None:
        self.key: UnitConversionKey = key

    def __str__(self) -> str:
        return f"The unit conversion {self.key} was not found."


class DuplicateUnitConversionError(UnitConversionError):
    """Raised when a duplicate unit conversion is added."""

    def __init__(self, key: UnitConversionKey):
        self.key = key

    def __str__(self) -> str:
        return f"The unit conversion {self.key} already exists on the entity."


class ZeroQuantityInUCError(UnitConversionError):
    """Raised when a unit conversion has a zero quantity."""

    def __init__(self, key: UnitConversionKey) -> None:
        self.key: UnitConversionKey = key

    def __str__(self) -> str:
        return f"The unit conversion {self.key} has a zero quantity."


class NegativeQuantityInUCError(UnitConversionError):
    """Raised when a unit conversion has a negative quantity."""

    def __init__(self, key: UnitConversionKey) -> None:
        self.key: UnitConversionKey = key

    def __str__(self) -> str:
        return f"The unit conversion {self.key} has a negative quantity."


class SameUnitConversionError(UnitConversionError):
    """Raised when a unit conversion has the same from and to units."""

    def __init__(self, key: UnitConversionKey) -> None:
        self.key: UnitConversionKey = key

    def __str__(self) -> str:
        return f"The unit conversion {self.key} has the same from and to units."


class UndefinedUnitConversionError(UnitConversionError):
    """Raised when the unit conversion is not defined on the entity."""

    def __init__(self, key: UnitConversionKey) -> None:
        self.key: UnitConversionKey = key

    def __str__(self) -> str:
        return f"The unit conversion {self.key} is not defined on the entity."


class UnitConversionOverconstrainedError(UnitConversionError):
    """Raised when the unit conversion would overconstrain the entity."""

    def __init__(self, key: UnitConversionKey):
        self.key = key

    def __str__(self) -> str:
        return f"The unit conversion {self.key} would overconstrain the entity."


__all__ = [
    "UnitError",
    "UnknownUnitError",
    "QuantityError",
    "NegativeQuantityError",
    "ZeroQuantityError",
    "UnitConversionError",
    "UnitConversionNotFoundError",
    "DuplicateUnitConversionError",
    "ZeroQuantityInUCError",
    "NegativeQuantityInUCError",
    "SameUnitConversionError",
    "UndefinedUnitConversionError",
    "UnitConversionOverconstrainedError",
]
