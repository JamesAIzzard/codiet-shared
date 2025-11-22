from __future__ import annotations

from .common import CodietException


class CostError(CodietException):
    """Base class for all cost-related exceptions."""


class NegativeCostError(CostError):
    """Raised when a cost value is negative."""

    def __init__(self, cost_value: float) -> None:
        self.cost_value = cost_value

    @property
    def message(self) -> str:
        return f"Cost value cannot be negative: {self.cost_value}."


__all__ = [
    "CostError",
    "NegativeCostError",
]
