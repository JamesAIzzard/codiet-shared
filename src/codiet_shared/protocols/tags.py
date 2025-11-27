from __future__ import annotations
from typing import Protocol, runtime_checkable, Mapping

from pygraph import GraphNode

from ..exceptions.tags import TagNotFoundError


@runtime_checkable
class Tag(GraphNode, Protocol):
    @property
    def uid(self) -> int: ...

    @property
    def name(self) -> str: ...


TagMap = Mapping[int, Tag]


class HasTags(Protocol):
    @property
    def tags(self) -> TagMap: ...

    def has_tag(self, tag_uid: int) -> bool:
        return tag_uid in self.tags

    def assert_has_tag(self, tag_uid: int) -> None:
        if not self.has_tag(tag_uid):
            raise TagNotFoundError(tag_uid)

    def get_tag(self, tag_uid: int) -> Tag:
        self.assert_has_tag(tag_uid)
        return self.tags[tag_uid]


__all__ = [
    "Tag",
    "TagMap",
    "HasTags",
]
