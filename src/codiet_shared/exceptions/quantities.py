from __future__ import annotations
from typing import TYPE_CHECKING

from ..exceptions.common import CodietException

if TYPE_CHECKING:
    from ..protocols.quantities import UnitConversionKey


class UnitError(CodietException):
    """Base Unit error."""


class UnknownUnitError(UnitError):
    """A unit is unknown to the system."""

    def __init__(self, key: str) -> None:
        self.key: str = key

    @property
    def message(self) -> str:
        return f"The unit {self.key} is unknown to the system."


class QuantityError(CodietException):
    """General base class for quantity errors."""


class NegativeQuantityError(QuantityError):
    """Raised when a quantity is negative."""

    def __init__(self, quantity: float):
        self.quantity = quantity

    @property
    def message(self) -> str:
        return f"The quantity is negative: {self.quantity}."


class ZeroQuantityError(QuantityError):
    """Raised when a quantity is zero."""

    @property
    def message(self) -> str:
        return "The quantity is zero."


class UnitConversionError(CodietException):
    """Base class for unit conversion errors."""


class DuplicateUnitConversionError(UnitConversionError):
    """Raised when a duplicate unit conversion is added."""

    def __init__(self, key: UnitConversionKey):
        self.key = key

    @property
    def message(self) -> str:
        return f"The unit conversion {self.key} already exists on the entity."


class UndefinedUnitConversionError(UnitConversionError):
    """Raised when the unit conversion is not defined on the entity."""

    def __init__(self, key: UnitConversionKey) -> None:
        self.key: UnitConversionKey = key

    @property
    def message(self) -> str:
        return f"The unit conversion {self.key} is not defined on the entity."


class UnitConversionOverconstrainedError(UnitConversionError):
    """Raised when the unit conversion would overconstrain the entity."""

    def __init__(self, key: UnitConversionKey):
        self.key = key

    @property
    def message(self) -> str:
        return f"The unit conversion {self.key} would overconstrain the entity."
