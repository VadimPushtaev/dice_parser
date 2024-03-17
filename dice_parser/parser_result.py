import typing
from dataclasses import dataclass
from typing import Callable
from dice_parser.modifier import DiceModifier


NumberParseResultT = typing.TypeVar('NumberParseResultT', bound='NumberParseResult')


@dataclass
class ParseResult:
    value: int
    string: str


@dataclass
class ModifierParseResult:
    modifier: DiceModifier


class NumberParseResult:
    def __init__(
        self,
        value: int,
        string: str,
        flag: str | None = None,
    ) -> None:
        self.value: int = value
        self.string: str = string
        self.flag: str | None = flag

    def to_public_result(self) -> ParseResult:
        assert isinstance(self.value, int)
        assert isinstance(self.string, str)
        return ParseResult(self.value, self.string)

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(
            type(self).__name__,
            repr(self.value),
            repr(self.string),
            repr(self.flag)
        )

    @classmethod
    def binary_operator(
        cls: typing.Type[NumberParseResultT],
        left: 'NumberParseResult',
        right: 'NumberParseResult',
        operator_callable: Callable[[int, int], int],
        template: str,
    ) -> NumberParseResultT:
        return cls(
            operator_callable(left.value, right.value),
            template.format(left.string, right.string),
        )

    @classmethod
    def unary_operator(
        cls: typing.Type[NumberParseResultT],
        value: 'NumberParseResult',
        operator_callable: Callable[[int], int],
        template: str,
    ) -> NumberParseResultT:
        return cls(
            operator_callable(value.value),
            template.format(value.string),
        )
