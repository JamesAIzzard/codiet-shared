from codiet_shared.exceptions import CodietException


class TagError(CodietException):
    """Base class for all tag-related exceptions."""


class UnknownTagError(TagError):
    """Raised when a tag is unknown to the system."""

    def __init__(self, key: str) -> None:
        self.key: str = key

    @property
    def message(self) -> str:
        return f"The tag {self.key} is unknown to the system."


class TagNotFoundError(TagError):
    def __init__(self, uid: int) -> None:
        self.uid: int = uid

    @property
    def message(self) -> str:
        return f"The tag {self.uid} was not found on the entity."


class DuplicateTagError(TagError):
    def __init__(self, uid: int) -> None:
        self.uid = uid

    @property
    def message(self) -> str:
        return f"The tag {self.uid} already exists on the entity."

__all__ = [
    "TagError",
    "UnknownTagError",
    "TagNotFoundError",
    "DuplicateTagError",
]
