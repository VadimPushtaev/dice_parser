import typing
from dataclasses import dataclass
from typing import Callable

from lark import v_args

from dice_parser.modifier import DiceModifier

NumberParseResultT = typing.TypeVar('NumberParseResultT', bound='NumberParseResult')


class OperatorCallableResultT(typing.Protocol):
    def __call__(self, *args: 'NumberParseResult') -> 'NumberParseResult':
        ...

 
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
    def operator(
        cls: type[NumberParseResultT],
        operator_callable: typing.Any,
        template: str,
    ) -> Callable[[typing.Any], OperatorCallableResultT]:
        @v_args(inline=True)
        def result(
            decorated_self: typing.Any,
            *args: NumberParseResult,
        ) -> NumberParseResult:
            return cls(
                operator_callable(*(x.value for x in args)),
                template.format(*(x.string for x in args)),
            )

        return result
