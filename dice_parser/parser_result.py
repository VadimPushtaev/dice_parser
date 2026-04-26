"""Internal and public parser result objects."""

import typing
from dataclasses import dataclass
from typing import Callable

from dice_parser.modifier import DiceModifier

NumberParseResultT = typing.TypeVar("NumberParseResultT", bound="NumberParseResult")


@dataclass
class ParseResult:
    """Public parser result."""

    value: int
    string: str


@dataclass
class ModifierParseResult:
    """Parser result carrying a dice modifier."""

    modifier: DiceModifier


class NumberParseResult:
    """Internal parser result carrying a value, string, and optional flag."""

    def __init__(
        self,
        value: int,
        string: str,
        flag: str | None = None,
    ) -> None:
        """Initialize the internal number result."""
        self.value: int = value
        self.string: str = string
        self.flag: str | None = flag

    def to_public_result(self) -> ParseResult:
        """Convert this internal result to a public result."""
        assert isinstance(self.value, int)
        assert isinstance(self.string, str)
        return ParseResult(self.value, self.string)

    def __repr__(self) -> str:
        """Return a debug representation of this result."""
        return f"{type(self).__name__}({self.value!r}, {self.string!r}, {self.flag!r})"

    @classmethod
    def binary_operator(
        cls: typing.Type[NumberParseResultT],
        left: "NumberParseResult",
        right: "NumberParseResult",
        operator_callable: Callable[[int, int], int],
        template: str,
    ) -> NumberParseResultT:
        """Build a result from a binary operation."""
        return cls(
            operator_callable(left.value, right.value),
            template.format(left.string, right.string),
        )

    @classmethod
    def unary_operator(
        cls: typing.Type[NumberParseResultT],
        value: "NumberParseResult",
        operator_callable: Callable[[int], int],
        template: str,
    ) -> NumberParseResultT:
        """Build a result from a unary operation."""
        return cls(
            operator_callable(value.value),
            template.format(value.string),
        )
