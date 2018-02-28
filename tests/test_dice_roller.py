from unittest import TestCase

from dice_parser import DiceModifier


class DiceRollerTestCase(TestCase):
    def test__safe_count(self):
        self.assertEqual(DiceModifier(-3)._safe_count([1, 2]), 0)
        self.assertEqual(DiceModifier(0)._safe_count([1, 2]), 0)
        self.assertEqual(DiceModifier(2)._safe_count([1, 2]), 2)
        self.assertEqual(DiceModifier(5)._safe_count([1, 2]), 2)


