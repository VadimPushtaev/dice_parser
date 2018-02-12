# dice_parser
Arithmetic expressions with dice roll support
    @classmethod
    def _roll_die(cls, size):
        return 1 + randrange(0, size)

    def _add_flag(self, result, flag):
        return ParseResult(result.value, result.string, result.dice, flag)

