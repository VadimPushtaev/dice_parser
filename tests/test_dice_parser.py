from unittest import TestCase

from dice_parser import DiceParser, Transformer


class DiceExpressionTestCase(TestCase):
    def setUp(self):
        self.parser = DiceParser()

    def test_simple(self):
        result = self.parser.parse('3*4 + 12/3 + ( 3-2 )')
        self.assertEqual(result.value, 17)
        self.assertEqual(result.string, '3 * 4 + 12 / 3 + (3 - 2)')
        self.assertEqual(result.dice, [])

    def test_dice(self):
        Transformer._roll_die = lambda cls_, size: int(size)
        result = self.parser.parse('d10 * 3 + 2d + ( 3d30 )')
        self.assertEqual(result.value, 160)
        self.assertEqual(result.string, '[10] * 3 + [20, 20] + ([30, 30, 30])')
        self.assertEqual(result.dice, [10, 20, 20, 30, 30, 30])

    def test_vars(self):
        Transformer._roll_die = lambda cls_, size: int(size)
        result = self.parser.parse('a=2+2')
        self.assertEqual(result.value, 4)
        self.assertEqual(result.string, 'a = 2 + 2')
        self.assertEqual(result.dice, [])

        result = self.parser.parse('4*a')
        self.assertEqual(result.value, 16)
        self.assertEqual(result.string, '4 * a')
        self.assertEqual(result.dice, [])
