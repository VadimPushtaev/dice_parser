# dice_parser
Arithmetic expressions with dice roll support

## Installation

`pip install dice_parser`

## Usage

```python
In [1]: from dice_parser import DiceParser

In [2]: parser = DiceParser()

In [3]: parser.parse('2d6 + 4')
Out[3]: ParseResult(8, '[3, 1] + 4', None)
```
