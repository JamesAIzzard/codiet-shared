from typing import Any


class CodietException(Exception):
    """Base exception for Codiet-related errors."""

    def __str__(self) -> str:
        return self.message

    @property
    def message(self) -> str:
        return self.__class__.__name__


class InvalidDTOError(CodietException):
    """Raised when a DTO is invalid."""

    def __init__(self, dto: Any) -> None:
        self.dto = dto

    @property
    def message(self) -> str:
        return f"Invalid DTO: {self.dto}"
