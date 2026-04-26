"""Roll dice and apply dice modifiers."""

import random

from dice_parser.modifier import DiceModifier

GAME_RANDOM = random.Random()  # noqa: S311


def roll_game_die(size: int) -> int:
    """Roll a die with non-cryptographic game randomness."""
    return GAME_RANDOM.randrange(1, 1 + size) if size > 0 else 0


class DiceRoller:
    """Roll a fixed number of dice with a modifier."""

    def __init__(self, count: int, size: int, modifier: DiceModifier) -> None:
        """Initialize the roller with dice count, size, and modifier."""
        self._count: int = count
        self._size: int = size
        self._modifier: DiceModifier = modifier

    def roll(self) -> tuple[int, list[int]]:
        """Roll dice and return the modified total with all rolled values."""
        rolled = [self._roll_die(self._size) for _ in range(self._count)]
        actual, _ignored = self._modifier.get_actual_dice(rolled)

        return sum(actual), rolled

    @staticmethod
    def _roll_die(size: int) -> int:
        return roll_game_die(size)
