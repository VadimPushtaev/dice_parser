from itertools import chain
from unittest import TestCase

from dice_parser.dice_roller import DiceRoller
from dice_parser.parser import DiceParser


class DiceExpressionTestCase(TestCase):
    def setUp(self) -> None:
        self.parser = DiceParser()
        DiceRoller._roll_die = lambda cls_, size: size

    def test_simple(self) -> None:
        result = self.parser.parse("3*4 + 12/3 + ( 3-2 )")
        assert result.value == 17
        assert result.string == "3 * 4 + 12 / 3 + (3 - 2)"

    def test_dice(self) -> None:
        result = self.parser.parse("d10 * 3 + 2D + ( 3 D 30 )")
        assert result.value == 160
        assert result.string == "[10] * 3 + [20, 20] + ([30, 30, 30])"

    def test_dice__invalid_size(self) -> None:
        result = self.parser.parse("3d0")
        assert result.value == 0
        assert result.string == "[0, 0, 0]"
        result = self.parser.parse("2d(-1)")
        assert result.value == 0
        assert result.string == "[0, 0]"

    def test_dice__invalid_count(self) -> None:
        result = self.parser.parse("0d3")
        assert result.value == 0
        assert result.string == "[]"
        result = self.parser.parse("(-3)d3")
        assert result.value == 0
        assert result.string == "[]"

    def test_dice__dynamic(self) -> None:
        result = self.parser.parse("(2+2) d (3*3)+1")
        assert result.value == 37
        assert result.string == "[9, 9, 9, 9] + 1"

    def test_dice__modifier(self) -> None:
        rolled = iter(
            chain(
                (1, 6, 5, 4, 3, 2),  # 6d6
                (1,),  # L(1d20)
                (20, 15),  # 2d20
            ),
        )
        DiceRoller._roll_die = lambda cls_, size: next(rolled)

        result = self.parser.parse("6d6h3 + 2d20L(1d1)")
        assert result.value == 30
        assert result.string == "[1, 6, 5, 4, 3, 2] + [20, 15]"

    def test_dice__strange_modifier(self) -> None:
        assert self.parser.parse("3d10H5").value == 30
        assert self.parser.parse("3d10H0").value == 0
        assert self.parser.parse("3d10H(-1)").value == 0
        assert self.parser.parse("3d10L5").value == 30
        assert self.parser.parse("3d10L0").value == 0
        assert self.parser.parse("3d10L(-1)").value == 0

    def test_vars(self) -> None:
        result = self.parser.parse("a=2+2")
        assert result.value == 4
        assert result.string == "a = 2 + 2"

        result = self.parser.parse("d a")
        assert result.value == 4
        assert result.string == "[4]"
