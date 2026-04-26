from unittest import TestCase

from dice_parser.modifier import DiceModifier


class SomeDiceModifier(DiceModifier):
    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        pass


class DiceRollerTestCase(TestCase):
    def test__safe_count(self):
        assert SomeDiceModifier(-3)._safe_count([1, 2]) == 0
        assert SomeDiceModifier(0)._safe_count([1, 2]) == 0
        assert SomeDiceModifier(2)._safe_count([1, 2]) == 2
        assert SomeDiceModifier(5)._safe_count([1, 2]) == 2
