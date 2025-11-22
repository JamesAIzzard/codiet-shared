from __future__ import annotations
from typing import Protocol, runtime_checkable, Mapping, Optional

from pygraph import GraphNode

from ..exceptions.tags import TagNotFoundError


@runtime_checkable
class Tag(GraphNode, Protocol):
    @property
    def uid(self) -> Optional[int]: ...


TagMap = Mapping[str, Tag]


class HasTags(Protocol):
    @property
    def tags(self) -> TagMap: ...

    def has_tag(self, tag_name: str) -> bool:
        return tag_name in self.tags

    def assert_has_tag(self, tag_name: str) -> None:
        if not self.has_tag(tag_name):
            raise TagNotFoundError(tag_name)

    def get_tag(self, tag_name: str) -> Tag:
        self.assert_has_tag(tag_name)
        return self.tags[tag_name]


__all__ = [
    "Tag",
    "TagMap",
    "HasTags",
]
