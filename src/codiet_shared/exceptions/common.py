from typing import Any


class CodietException(Exception):
    """Base exception for all codiet exceptions.""" 

class InvalidDTOError(CodietException):
    """Raised when a DTO is invalid."""

    def __init__(self, dto: Any) -> None:
        super().__init__(f"Invalid DTO: {dto}")