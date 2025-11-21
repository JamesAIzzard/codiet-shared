from __future__ import annotations
from typing import Any, TypeGuard, TypedDict
import numbers

from .dto_predicates import has_only_keys


class CostRatioDTO(TypedDict):
    host_quantity_unit: str
    host_quantity_value: float
    cost: float


def is_cost_ratio_dto(obj: Any) -> TypeGuard[CostRatioDTO]:
    return (
        isinstance(obj, dict)
        and has_only_keys(obj, ("host_quantity_unit", "host_quantity_value", "cost"))
        and isinstance(obj.get("host_quantity_unit"), str)
        and isinstance(obj.get("host_quantity_value"), numbers.Real)
        and isinstance(obj.get("cost"), numbers.Real)
    )
