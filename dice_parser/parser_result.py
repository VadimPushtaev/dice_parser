"""Internal and public parser result objects."""

import typing
from collections.abc import Callable
from dataclasses import dataclass
from typing import override

from dice_parser.modifier import DiceModifier
from dice_parser.type_helpers import ensure_type


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
        return ParseResult(
            ensure_type(self.value, int, "value"),
            ensure_type(self.string, str, "string"),
        )

    @override
    def __repr__(self) -> str:
        """Return a debug representation of this result."""
        return f"{type(self).__name__}({self.value!r}, {self.string!r}, {self.flag!r})"

    @classmethod
    def binary_operator(
        cls,
        left: "NumberParseResult",
        right: "NumberParseResult",
        operator_callable: Callable[[int, int], int],
        template: str,
    ) -> typing.Self:
        """Build a result from a binary operation."""
        return cls(
            operator_callable(left.value, right.value),
            template.format(left.string, right.string),
        )

    @classmethod
    def unary_operator(
        cls,
        value: "NumberParseResult",
        operator_callable: Callable[[int], int],
        template: str,
    ) -> typing.Self:
        """Build a result from a unary operation."""
        return cls(
            operator_callable(value.value),
            template.format(value.string),
        )
