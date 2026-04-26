# dice_parser

Arithmetic expressions with dice roll support.

`dice_parser` evaluates integer arithmetic expressions and common tabletop dice
notation such as `d20`, `2d6`, `6d6h3`, and `2d20L(1d1)`. It also keeps a
readable representation of the rolls used to compute the final value.

## Installation

```bash
pip install dice-parser
```

## Usage

```python
from dice_parser.parser import DiceParser

parser = DiceParser()

result = parser.parse("2d6 + 4")

print(result.value)
print(result.string)
```

The result is a `ParseResult` object with two fields:

- `value`: the evaluated integer value.
- `string`: a readable expression showing the dice that were rolled.

## Supported Syntax

```python
parser.parse("3 * 4 + 12 / 3 + (3 - 2)")
parser.parse("d20")
parser.parse("2d6 + 4")
parser.parse("6d6h3")
parser.parse("2d20L(1d1)")
parser.parse("a=2+2")
parser.parse("d a")
```
