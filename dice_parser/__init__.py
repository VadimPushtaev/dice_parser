import operator
from functools import wraps
from random import randrange

from lark import Lark, InlineTransformer


class ParseResult:
    def __init__(self, value, string, dice, flag=None):
        self.value = value
        self.string = string
        self.dice = dice
        self.flag = flag

    def __repr__(self):
        return '{}({}, {}, {}, {})'.format(
            type(self).__name__,
            repr(self.value),
            repr(self.string),
            repr(self.dice),
            repr(self.flag)
        )

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

    def roll(self, *args):
        count = 1
        size = 20
        for arg in args:
            if arg.flag == 'left':
                count = arg.value
            if arg.flag == 'right':
                size = arg.value

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

    def left_atom(self, atom):
        return ParseResult(atom.value, atom.string, atom.dice, 'left')

    def right_atom(self, atom):
        return ParseResult(atom.value, atom.string, atom.dice, 'right')


class DiceParser:
    GRAMMAR = """
        NAME: /[a-z_]+/

        ?start: sum
            | NAME "=" sum     -> assign_var

        ?sum: product
            | sum "+" product  -> add
            | sum "-" product  -> sub

        ?product: die
            | product "*" die  -> mul
            | product "/" die  -> div
        
        ?die: atom
            | left_atom? "d" right_atom?  -> roll  

        ?atom: /\d+/           -> number
            | "-" atom         -> neg
            | NAME             -> var
            | "(" sum ")"      -> brackets

        left_atom: atom -> left_atom
        right_atom: atom -> right_atom
        
        %import common.WS_INLINE
        %ignore WS_INLINE
    """

    def __init__(self):
        self._parser = Lark(self.GRAMMAR, parser='lalr', transformer=Transformer())

    def parse(self, string):
        return self._parser.parse(string)