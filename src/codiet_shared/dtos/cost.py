from __future__ import annotations
from typing import Any, TypeGuard, TypedDict
import numbers

from .utils import has_only_keys


class CostRatioDTO(TypedDict):
    host_quantity_unit_uid: int
    host_quantity_value: float
    cost: float


def is_cost_ratio_dto(obj: Any) -> TypeGuard[CostRatioDTO]:
    return (
        isinstance(obj, dict)
        and has_only_keys(obj, ("host_quantity_unit_uid", "host_quantity_value", "cost"))
        and isinstance(obj.get("host_quantity_unit_uid"), int)
        and isinstance(obj.get("host_quantity_value"), numbers.Real)
        and isinstance(obj.get("cost"), numbers.Real)
    )
