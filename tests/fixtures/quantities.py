"""Pytest fixtures for quantities DTOs."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from codiet_shared.dtos.quantities import (
        QuantityDTO,
        UnitConversionDTO,
        UnitDTO,
    )


@pytest.fixture
def sample_unit_dto() -> UnitDTO:
    """Provide a valid UnitDTO for testing."""
    return {
        "uid": 1,
        "name": "gram",
        "unit_type": "mass",
        "unit_system": "metric",
        "singular_abbreviation": "g",
        "plural_abbreviation": "g",
        "aliases": ["grams", "gramme"],
    }


@pytest.fixture
def sample_unit_conversion_dto() -> UnitConversionDTO:
    """Provide a valid UnitConversionDTO for testing."""
    return {
        "uid": 1,
        "from_unit_uid": 1,
        "from_unit_value": 1.0,
        "to_unit_uid": 2,
        "to_unit_value": 1000.0,
    }


@pytest.fixture
def sample_quantity_dto() -> QuantityDTO:
    """Provide a valid QuantityDTO for testing."""
    return {
        "unit_uid": 1,
        "value": 100.0,
    }
