from __future__ import annotations
from typing import Protocol, runtime_checkable

from .quantities import IsQuantified
from ..dtos.cost import CostRatioDTO


@runtime_checkable
class CostRatio(Protocol):
    @property
    def cost_per_gram(self) -> float: ...

    def to_dto(self) -> CostRatioDTO: ...

    def __str__(self) -> str:
        return f"£{self.cost_per_gram:.2f}/g"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.cost_per_gram)

    def __eq__(self, other) -> bool:
        if not isinstance(other, CostRatio):
            return NotImplemented
        return hash(self) == hash(other)


class HasCostRatio(Protocol):
    @property
    def cost_ratio(self) -> CostRatio: ...


class HasCost(IsQuantified, HasCostRatio, Protocol):
    @property
    def total_cost(self) -> float:
        return self.quantity.mass_in_grams * self.cost_ratio.cost_per_gram


__all__ = [
    "CostRatio",
    "HasCostRatio",
    "HasCost",
]
