"""Tests for dice expression parsing."""

from itertools import chain
from typing import override
from unittest import TestCase
from unittest.mock import patch

from dice_parser.dice_roller import DiceRoller
from dice_parser.parser import DiceParser


class DiceExpressionTestCase(TestCase):
    """Test dice expression parsing."""

    @override
    def setUp(self) -> None:
        """Create a parser that rolls the maximum value by default."""
        self.parser = DiceParser()

        def roll_max(size: int) -> int:
            return size

        roll_patcher = patch.object(DiceRoller, "_roll_die", staticmethod(roll_max))
        roll_patcher.start()
        self.addCleanup(roll_patcher.stop)

    def test_simple(self) -> None:
        """Parse plain arithmetic."""
        result = self.parser.parse("3*4 + 12/3 + ( 3-2 )")
        assert result.value == 17
        assert result.string == "3 * 4 + 12 / 3 + (3 - 2)"

    def test_dice(self) -> None:
        """Parse simple dice expressions."""
        result = self.parser.parse("d10 * 3 + 2D + ( 3 D 30 )")
        assert result.value == 160
        assert result.string == "[10] * 3 + [20, 20] + ([30, 30, 30])"

    def test_dice__invalid_size(self) -> None:
        """Parse dice with invalid sizes."""
        result = self.parser.parse("3d0")
        assert result.value == 0
        assert result.string == "[0, 0, 0]"
        result = self.parser.parse("2d(-1)")
        assert result.value == 0
        assert result.string == "[0, 0]"

    def test_dice__invalid_count(self) -> None:
        """Parse dice with invalid counts."""
        result = self.parser.parse("0d3")
        assert result.value == 0
        assert result.string == "[]"
        result = self.parser.parse("(-3)d3")
        assert result.value == 0
        assert result.string == "[]"

    def test_dice__dynamic(self) -> None:
        """Parse dice with dynamic count and size expressions."""
        result = self.parser.parse("(2+2) d (3*3)+1")
        assert result.value == 37
        assert result.string == "[9, 9, 9, 9] + 1"

    def test_dice__modifier(self) -> None:
        """Parse dice modifiers."""
        rolled = iter(
            chain(
                (1, 6, 5, 4, 3, 2),  # 6d6
                (1,),  # L(1d20)
                (20, 15),  # 2d20
            ),
        )

        def roll_next(size: int) -> int:
            del size
            return next(rolled)

        with patch.object(DiceRoller, "_roll_die", staticmethod(roll_next)):
            result = self.parser.parse("6d6h3 + 2d20L(1d1)")
        assert result.value == 30
        assert result.string == "[1, 6, 5, 4, 3, 2] + [20, 15]"

    def test_dice__strange_modifier(self) -> None:
        """Parse out-of-range dice modifiers."""
        assert self.parser.parse("3d10H5").value == 30
        assert self.parser.parse("3d10H0").value == 0
        assert self.parser.parse("3d10H(-1)").value == 0
        assert self.parser.parse("3d10L5").value == 30
        assert self.parser.parse("3d10L0").value == 0
        assert self.parser.parse("3d10L(-1)").value == 0

    def test_vars(self) -> None:
        """Parse variable assignment and references."""
        result = self.parser.parse("a=2+2")
        assert result.value == 4
        assert result.string == "a = 2 + 2"

        result = self.parser.parse("d a")
        assert result.value == 4
        assert result.string == "[4]"
