"""Tests for dice rolling helpers."""

from unittest import TestCase

from dice_parser.modifier import DiceModifier


class SomeDiceModifier(DiceModifier):
    """Concrete dice modifier for base-class tests."""

    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        """Return no dice."""


class DiceRollerTestCase(TestCase):
    """Test dice rolling helpers."""

    def test__safe_count(self) -> None:
        """Clamp modifier counts to the available dice."""
        assert SomeDiceModifier(-3)._safe_count([1, 2]) == 0
        assert SomeDiceModifier(0)._safe_count([1, 2]) == 0
        assert SomeDiceModifier(2)._safe_count([1, 2]) == 2
        assert SomeDiceModifier(5)._safe_count([1, 2]) == 2
