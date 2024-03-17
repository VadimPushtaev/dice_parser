import operator

from lark import Transformer, v_args

from dice_parser.dice_roller import DiceRoller
from dice_parser.modifier import DiceModifier
from dice_parser.parser_result import NumberParseResult, ModifierParseResult


class NullDiceModifier(DiceModifier):
    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        return dice, []


class HighestDiceModifier(DiceModifier):
    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        sorted_dice = sorted(dice)
        count = self._safe_count(dice)
        n = len(sorted_dice)

        return sorted_dice[n - count:], sorted_dice[:n - count]


class LowestDiceModifier(DiceModifier):
    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        sorted_dice = sorted(dice)
        count = self._safe_count(dice)

        return sorted_dice[:count], sorted_dice[count:]


class DiceTransformer(Transformer[NumberParseResult, int]):
    def __init__(self) -> None:
        super().__init__()
        self.vars: dict[str, NumberParseResult] = {}

    @v_args(inline=True)
    def add(self, left: NumberParseResult, right: NumberParseResult) -> NumberParseResult:
        return NumberParseResult.binary_operator(
            left, right, operator.add, '{} + {}'
        )

    @v_args(inline=True)
    def sub(self, left: NumberParseResult, right: NumberParseResult) -> NumberParseResult:
        return NumberParseResult.binary_operator(
            left, right, operator.sub, '{} - {}'
        )

    @v_args(inline=True)
    def mul(self, left: NumberParseResult, right: NumberParseResult) -> NumberParseResult:
        return NumberParseResult.binary_operator(
            left, right, operator.mul, '{} * {}'
        )

    @v_args(inline=True)
    def div(self, left: NumberParseResult, right: NumberParseResult) -> NumberParseResult:
        return NumberParseResult.binary_operator(
            left, right, operator.floordiv, '{} / {}'
        )

    @v_args(inline=True)
    def neg(self, result: NumberParseResult) -> NumberParseResult:
        return NumberParseResult.unary_operator(
            result, operator.neg, '-{}'
        )

    @v_args(inline=True)
    def number(self, value: str) -> NumberParseResult:
        return NumberParseResult(int(value), str(int(value)), None)

    @v_args(inline=True)
    def dice_count(self, result: NumberParseResult) -> NumberParseResult:
        return self._add_flag(result, 'dice_count')

    @v_args(inline=True)
    def dice_size(self, result: NumberParseResult) -> NumberParseResult:
        if result.value < 1:
            result.value = 0
        return self._add_flag(result, 'dice_size')

    @v_args(inline=True)
    def dice_highest(self, result: NumberParseResult) -> ModifierParseResult:
        return ModifierParseResult(HighestDiceModifier(int(result.value)))

    @v_args(inline=True)
    def dice_lowest(self, result: NumberParseResult) -> ModifierParseResult:
        return ModifierParseResult(LowestDiceModifier(int(result.value)))

    @v_args(inline=True)
    def brackets(self, result: NumberParseResult) -> NumberParseResult:
        return NumberParseResult(result.value, '({})'.format(result.string))

    @v_args(inline=True)
    def roll(self, *args: NumberParseResult | ModifierParseResult) -> NumberParseResult:
        # default is 1d20
        count = 1
        size = 20

        modifier: DiceModifier = NullDiceModifier()
        for arg in args:
            if isinstance(arg, ModifierParseResult):
                modifier = arg.modifier
            else:
                if arg.flag == 'dice_count':
                    count = arg.value
                if arg.flag == 'dice_size':
                    size = arg.value

        roller = DiceRoller(count, size, modifier)
        rolled_result, rolled_dice = roller.roll()

        return NumberParseResult(
            rolled_result,
            '[{}]'.format(', '.join(str(d) for d in rolled_dice)),
        )

    @v_args(inline=True)
    def assign_var(self, name: str, result: NumberParseResult) -> NumberParseResult:
        self.vars[name] = NumberParseResult(
            result.value,
            name,
        )

        return NumberParseResult(
            result.value,
            '{} = {}'.format(name, result.string),
        )

    @v_args(inline=True)
    def var(self, name: str) -> NumberParseResult:
        return self.vars[name]

    @classmethod
    def _add_flag(cls, result: NumberParseResult, flag: str) -> NumberParseResult:
        return NumberParseResult(result.value, result.string, flag)
