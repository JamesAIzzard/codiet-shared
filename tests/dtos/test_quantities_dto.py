"""Tests for quantities DTO type guards."""

from __future__ import annotations

from typing import TYPE_CHECKING

from codiet_shared.dtos.quantities import (
    is_unit_dto,
    is_unit_conversion_dto,
    is_quantity_dto,
)

if TYPE_CHECKING:
    from codiet_shared.dtos.quantities import UnitDTO, UnitConversionDTO, QuantityDTO


class TestIsUnitDTO:
    """Tests for the is_unit_dto type guard."""

    def test_valid_unit_dto(self, sample_unit_dto: UnitDTO) -> None:
        """Verify returns True for a valid UnitDTO."""
        assert is_unit_dto(sample_unit_dto) is True

    def test_rejects_non_dict(self) -> None:
        """Verify returns False when given a non-dict value."""
        assert is_unit_dto("not a dict") is False
        assert is_unit_dto(123) is False
        assert is_unit_dto(None) is False

    def test_rejects_missing_keys(self) -> None:
        """Verify returns False when required keys are missing."""
        incomplete = {"uid": 1, "name": "gram"}
        assert is_unit_dto(incomplete) is False

    def test_rejects_wrong_uid_type(self, sample_unit_dto: UnitDTO) -> None:
        """Verify returns False when uid is not an int."""
        invalid = dict(sample_unit_dto)
        invalid["uid"] = "not-an-int"
        assert is_unit_dto(invalid) is False

    def test_rejects_wrong_aliases_type(self, sample_unit_dto: UnitDTO) -> None:
        """Verify returns False when aliases contains non-strings."""
        invalid = dict(sample_unit_dto)
        invalid["aliases"] = [1, 2, 3]
        assert is_unit_dto(invalid) is False


class TestIsUnitConversionDTO:
    """Tests for the is_unit_conversion_dto type guard."""

    def test_valid_unit_conversion_dto(
        self, sample_unit_conversion_dto: UnitConversionDTO
    ) -> None:
        """Verify returns True for a valid UnitConversionDTO."""
        assert is_unit_conversion_dto(sample_unit_conversion_dto) is True

    def test_accepts_none_uid(self) -> None:
        """Verify accepts None for the uid field."""
        dto = {
            "uid": None,
            "from_unit_uid": 1,
            "from_unit_value": 1.0,
            "to_unit_uid": 2,
            "to_unit_value": 1000.0,
        }
        assert is_unit_conversion_dto(dto) is True

    def test_rejects_non_dict(self) -> None:
        """Verify returns False when given a non-dict value."""
        assert is_unit_conversion_dto("not a dict") is False

    def test_rejects_missing_keys(self) -> None:
        """Verify returns False when required keys are missing."""
        incomplete = {"from_unit_uid": 1}
        assert is_unit_conversion_dto(incomplete) is False


class TestIsQuantityDTO:
    """Tests for the is_quantity_dto type guard."""

    def test_valid_quantity_dto(self, sample_quantity_dto: QuantityDTO) -> None:
        """Verify returns True for a valid QuantityDTO."""
        assert is_quantity_dto(sample_quantity_dto) is True

    def test_rejects_non_dict(self) -> None:
        """Verify returns False when given a non-dict value."""
        assert is_quantity_dto([1, 2]) is False

    def test_rejects_missing_keys(self) -> None:
        """Verify returns False when required keys are missing."""
        assert is_quantity_dto({"unit_uid": 1}) is False

    def test_rejects_wrong_value_type(self) -> None:
        """Verify returns False when value is not numeric."""
        invalid = {"unit_uid": 1, "value": "not a number"}
        assert is_quantity_dto(invalid) is False
