from __future__ import annotations
from typing import TYPE_CHECKING

from ..exceptions.common import CodietException

if TYPE_CHECKING:
    from ..protocols.quantities import UnitConversionKey


class UnitError(CodietException):
    """Base Unit error."""

    def __init__(self, message: str) -> None:
        self._message = message

    @property
    def message(self) -> str:
        return self._message


class UnknownUnitError(UnitError):
    def __init__(self, key: str) -> None:
        self.key: str = key

    @property
    def message(self) -> str:
        return f"The unit {self.key} is unknown to the system."


class QuantityError(CodietException):
    @property
    def message(self) -> str:
        return "General base class for quantity errors."


class NegativeQuantityError(QuantityError):
    def __init__(self, quantity: float):
        self.quantity = quantity

    @property
    def message(self) -> str:
        return f"The quantity is negative: {self.quantity}."


class ZeroQuantityError(QuantityError):
    @property
    def message(self) -> str:
        return "The quantity is zero."


class UnitConversionError(CodietException):
    """Base class for unit conversion errors."""

    def __init__(self, message: str) -> None:
        self._message = message

    @property
    def message(self) -> str:
        return self._message


class DuplicateUnitConversionError(UnitConversionError):
    def __init__(self, key: UnitConversionKey):
        self.key = key

    @property
    def message(self) -> str:
        return f"The unit conversion {self.key} already exists on the entity."


class UndefinedUnitConversionError(UnitConversionError):
    def __init__(self, key: UnitConversionKey) -> None:
        self.key: UnitConversionKey = key

    @property
    def message(self) -> str:
        return f"The unit conversion {self.key} is not defined on the entity."


class UnitConversionOverconstrainedError(UnitConversionError):
    def __init__(self, key: UnitConversionKey):
        self.key = key

    @property
    def message(self) -> str:
        return f"The unit conversion {self.key} would overconstrain the entity."
