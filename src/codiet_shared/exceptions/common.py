from typing import Any


class CodietError(Exception):
    """Base exception for all codiet exceptions.""" 

class InvalidDTOError(CodietError):
    """Raised when a DTO is invalid."""

    def __init__(self, dto: Any) -> None:
        super().__init__(f"Invalid DTO: {dto}")