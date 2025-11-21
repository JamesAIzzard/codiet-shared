from __future__ import annotations
from typing import TypedDict, Any, TypeGuard

from codiet_data.dto_predicates import has_only_keys


class TagDTO(TypedDict):
    uid: int | None
    name: str
    parents: list[str]


def is_tag_dto(obj: Any) -> TypeGuard[TagDTO]:
    if not isinstance(obj, dict):
        return False

    if not has_only_keys(obj, ("name", "parents", "uid")):
        return False

    if not isinstance(obj.get("name"), str):
        return False

    parents = obj.get("parents")
    if not isinstance(parents, list):
        return False
    if not all(isinstance(p, str) for p in parents):
        return False

    uid_val = obj.get("uid")
    if not (isinstance(uid_val, int) or uid_val is None):
        return False

    return True
