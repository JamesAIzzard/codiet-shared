class CodietException(Exception):
    """Base class for all Codiet-related exceptions."""

    def __str__(self) -> str:
        return "A Codiet-related error occurred."


class InvalidDTOError(CodietException):
    """Raised when a DTO is invalid."""

    def __init__(self, dto: dict) -> None:
        self.dto = dto

    def __str__(self) -> str:
        return f"Invalid DTO: {self.dto}"


__all__ = [
    "CodietException",
    "InvalidDTOError",
]
