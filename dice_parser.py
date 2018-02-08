import operator
from functools import wraps
from random import randrange

from lark import Lark, InlineTransformer


class ParseResult:
    def __init__(self, value, string, dice):
        self.value = value
        self.string = string
        self.dice = dice

    def __repr__(self):
        return '{}({}, {}, {})'.format(type(self).__name__, repr(self.value), repr(self.string), repr(self.dice))

    @classmethod
    def operator(cls, operator_callable, template):
        def decorator(method):
            @wraps(method)
            def decorated(decorated_self, *args):
                return cls(
                    operator_callable(*(x.value for x in args)),
                    template.format(*(x.string for x in args)),
                    sum((x.dice for x in args), [])
                )
            return decorated
        return decorator


class Transformer(InlineTransformer):
    def __init__(self):
        self.vars = {}

    def number(self, value):
        return ParseResult(int(value), str(int(value)), [])

    @ParseResult.operator(operator.add, '{} + {}')
    def add(self):
        pass

    @ParseResult.operator(operator.sub, '{} - {}')
    def sub(self):
        pass

    @ParseResult.operator(operator.mul, '{} * {}')
    def mul(self):
        pass

    @ParseResult.operator(operator.floordiv, '{} / {}')
    def div(self):
        pass

    @ParseResult.operator(operator.neg, '-{}')
    def neg(self):
        pass

    def brackets(self, result):
        return ParseResult(result.value, '({})'.format(result.string), result.dice)

    def roll(self, template):
        count_s, size_s = template.split('d')
        count = int(count_s) if count_s else 1
        size = int(size_s) if size_s else 20

        dice = []
        for _ in range(int(count)):
            dice.append(self._roll_die(size))

        return ParseResult(sum(dice), '[{}]'.format(', '.join(str(d) for d in dice)), dice)

    @classmethod
    def _roll_die(cls, size):
        return 1 + randrange(0, size)

    def assign_var(self, name, result):
        self.vars[name] = ParseResult(
            result.value,
            name,
            result.dice,
        )

        return ParseResult(
            result.value,
            '{} = {}'.format(name, result.string),
            result.dice,
        )

    def var(self, name):
        return self.vars[name]


class DiceParser:
    GRAMMAR = """
        NAME: /[a-z_]+/
    
        ?start: sum
              | NAME "=" sum    -> assign_var
    
        ?sum: product
            | sum "+" product   -> add
            | sum "-" product   -> sub
    
        ?product: atom
            | product "*" atom  -> mul
            | product "/" atom  -> div
    
        ?atom: /\d*d\d*/        -> roll
             | /\d+/            -> number
             | "-" atom         -> neg
             | NAME             -> var
             | "(" sum ")"      -> brackets
    
        %import common.WS_INLINE
        %ignore WS_INLINE
    """

    def __init__(self):
        self._parser = Lark(self.GRAMMAR, parser='lalr', transformer=Transformer())

    def parse(self, string):
        return self._parser.parse(string)