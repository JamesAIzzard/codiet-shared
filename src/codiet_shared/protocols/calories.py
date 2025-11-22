from __future__ import annotations
from typing import Protocol, runtime_checkable

from ..protocols.quantities import IsQuantified
from ..dtos.calories import CaloriesRatioDTO


@runtime_checkable
class CaloriesRatio(Protocol):
    @property
    def cals_per_gram(self) -> float: ...

    def to_dto(self) -> CaloriesRatioDTO: ...

    def __str__(self) -> str:
        return f"{self.cals_per_gram:.2f} kcal/g"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.cals_per_gram)

    def __eq__(self, other) -> bool:
        if not isinstance(other, CaloriesRatio):
            return NotImplemented
        return hash(self) == hash(other)


class HasCaloriesRatio(Protocol):
    @property
    def calories_ratio(self) -> CaloriesRatio: ...


class HasCalories(HasCaloriesRatio, IsQuantified, Protocol):
    @property
    def calories(self) -> float: ...


__all__ = [
    "CaloriesRatio",
    "HasCaloriesRatio",
    "HasCalories",
]
