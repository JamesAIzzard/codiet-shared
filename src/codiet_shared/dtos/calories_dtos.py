from __future__ import annotations
from typing import Any, TypeGuard, TypedDict
import numbers


from codiet_data.dto_predicates import has_only_keys
from codiet_data.dtos.quantity_dtos import QuantityDTO, is_quantity_dto


class CaloriesRatioDTO(TypedDict):
    host_quantity: QuantityDTO
    calories: float


def is_calories_ratio_dto(obj: Any) -> TypeGuard[CaloriesRatioDTO]:
    if not isinstance(obj, dict):
        return False

    if not has_only_keys(obj, ("host_quantity", "calories")):
        return False

    if not is_quantity_dto(obj["host_quantity"]):
        return False

    calories = obj["calories"]
    if not isinstance(calories, numbers.Real):
        return False

    return True
