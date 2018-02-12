from unittest import TestCase

from dice_parser import DiceParser, Transformer


class DiceExpressionTestCase(TestCase):
    def setUp(self):
        self.parser = DiceParser()
        Transformer._roll_die = lambda cls_, size: size

    def test_simple(self):
        result = self.parser.parse('3*4 + 12/3 + ( 3-2 )')
        self.assertEqual(result.value, 17)
        self.assertEqual(result.string, '3 * 4 + 12 / 3 + (3 - 2)')
        self.assertEqual(result.dice, [])

    def test_dice(self):
        result = self.parser.parse('d10 * 3 + 2d + ( 3 d 30 )')
        self.assertEqual(result.value, 160)
        self.assertEqual(result.string, '[10] * 3 + [20, 20] + ([30, 30, 30])')
        self.assertEqual(result.dice, [10, 20, 20, 30, 30, 30])

    def test_dice__dynamic(self):
        result = self.parser.parse('(2+2) d (3*3)+1')
        self.assertEqual(result.value, 37)
        self.assertEqual(result.string, '[9, 9, 9, 9] + 1')
        self.assertEqual(result.dice, [9, 9, 9, 9])

    def test_vars(self):
        result = self.parser.parse('a=2+2')
        self.assertEqual(result.value, 4)
        self.assertEqual(result.string, 'a = 2 + 2')
        self.assertEqual(result.dice, [])

        result = self.parser.parse('d a')
        self.assertEqual(result.value, 4)
        self.assertEqual(result.string, '[4]')
        self.assertEqual(result.dice, [4])

