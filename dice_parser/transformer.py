"""Transform parsed dice expression trees into parser results."""

from typing import override

from lark import Token, Transformer

from dice_parser.dice_roller import DiceRoller
from dice_parser.modifier import (
    DiceModifier,
    HighestDiceModifier,
    LowestDiceModifier,
    NullDiceModifier,
)
from dice_parser.parser_result import ModifierParseResult, NumberParseResult
from dice_parser.type_helpers import ensure_type


class DiceTransformer(Transformer[Token, NumberParseResult]):
    """Transform grammar callbacks into evaluated parse results."""

    @override
    def __init__(self) -> None:
        """Initialize variable storage."""
        super().__init__()
        self.vars: dict[str, NumberParseResult] = {}

    def add(self, children: list[NumberParseResult]) -> NumberParseResult:
        """Add two number results."""
        left, right = children
        return NumberParseResult(
            left.value + right.value,
            f"{left.string} + {right.string}",
        )

    def sub(self, children: list[NumberParseResult]) -> NumberParseResult:
        """Subtract two number results."""
        left, right = children
        return NumberParseResult(
            left.value - right.value,
            f"{left.string} - {right.string}",
        )

    def mul(self, children: list[NumberParseResult]) -> NumberParseResult:
        """Multiply two number results."""
        left, right = children
        return NumberParseResult(
            left.value * right.value,
            f"{left.string} * {right.string}",
        )

    def div(self, children: list[NumberParseResult]) -> NumberParseResult:
        """Divide two number results with floor division."""
        left, right = children
        return NumberParseResult(
            left.value // right.value,
            f"{left.string} / {right.string}",
        )

    def neg(self, children: list[NumberParseResult]) -> NumberParseResult:
        """Negate a number result."""
        (result,) = children
        return NumberParseResult(
            -result.value,
            f"-{result.string}",
        )

    def number(self, children: list[Token]) -> NumberParseResult:
        """Parse an integer token."""
        (value,) = children
        number = int(value)
        return NumberParseResult(number, str(number), None)

    def dice_count(self, children: list[NumberParseResult]) -> NumberParseResult:
        """Mark a result as a dice count."""
        (result,) = children
        return self._add_flag(result, "dice_count")

    def dice_size(self, children: list[NumberParseResult]) -> NumberParseResult:
        """Mark a result as a dice size."""
        (result,) = children
        value = max(0, result.value)
        return NumberParseResult(value, result.string, "dice_size")

    def dice_highest(self, children: list[NumberParseResult]) -> ModifierParseResult:
        """Build a highest-dice modifier result."""
        (result,) = children
        return ModifierParseResult(HighestDiceModifier(int(result.value)))

    def dice_lowest(self, children: list[NumberParseResult]) -> ModifierParseResult:
        """Build a lowest-dice modifier result."""
        (result,) = children
        return ModifierParseResult(LowestDiceModifier(int(result.value)))

    def brackets(self, children: list[NumberParseResult]) -> NumberParseResult:
        """Wrap a result string in brackets."""
        (result,) = children
        return NumberParseResult(result.value, f"({result.string})")

    def roll(
        self,
        children: list[NumberParseResult | ModifierParseResult],
    ) -> NumberParseResult:
        """Roll dice, defaulting to 1d20 when count or size is omitted."""
        count = 1
        size = 20

        modifier: DiceModifier = NullDiceModifier()
        for arg in children:
            if isinstance(arg, ModifierParseResult):
                modifier = arg.modifier
            else:
                if arg.flag == "dice_count":
                    count = arg.value
                if arg.flag == "dice_size":
                    size = arg.value

        roller = DiceRoller(count, size, modifier)
        rolled_result, rolled_dice = roller.roll()

        return NumberParseResult(
            rolled_result,
            "[{}]".format(", ".join(str(d) for d in rolled_dice)),
        )

    def assign_var(
        self,
        children: list[Token | NumberParseResult],
    ) -> NumberParseResult:
        """Assign a parsed result to a variable.

        Raises:
            TypeError: If parser children have unexpected runtime types.

        """
        name_token, result_value = children
        if isinstance(name_token, NumberParseResult):
            msg = f"name must be Token, got {type(name_token).__name__}"
            raise TypeError(msg)
        name = str(name_token)
        result = ensure_type(result_value, NumberParseResult, "result")
        self.vars[name] = NumberParseResult(
            result.value,
            name,
        )

        return NumberParseResult(
            result.value,
            f"{name} = {result.string}",
        )

    def var(self, children: list[Token]) -> NumberParseResult:
        """Return a previously assigned variable."""
        (name,) = children
        return self.vars[str(name)]

    @classmethod
    def _add_flag(cls, result: NumberParseResult, flag: str) -> NumberParseResult:
        return NumberParseResult(result.value, result.string, flag)
