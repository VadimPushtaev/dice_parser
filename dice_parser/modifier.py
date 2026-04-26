"""Dice roll modifiers."""

from abc import ABC, abstractmethod


class DiceModifier(ABC):
    """Base class for selecting actual and ignored dice."""

    def __init__(self, count: int = 0) -> None:
        """Initialize the modifier with the requested dice count."""
        self._count: int = count

    def _safe_count(self, dice: list[int]) -> int:
        return min(max(0, self._count), len(dice))

    @abstractmethod
    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        """Return the dice used for the total and the dice ignored."""


class NullDiceModifier(DiceModifier):
    """Use every rolled die."""

    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        """Return all dice as actual dice."""
        return dice, []


class HighestDiceModifier(DiceModifier):
    """Use the highest rolled dice."""

    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        """Return the highest dice as actual dice."""
        sorted_dice = sorted(dice)
        count = self._safe_count(dice)
        n = len(sorted_dice)

        return sorted_dice[n - count :], sorted_dice[: n - count]


class LowestDiceModifier(DiceModifier):
    """Use the lowest rolled dice."""

    def get_actual_dice(self, dice: list[int]) -> tuple[list[int], list[int]]:
        """Return the lowest dice as actual dice."""
        sorted_dice = sorted(dice)
        count = self._safe_count(dice)

        return sorted_dice[:count], sorted_dice[count:]
