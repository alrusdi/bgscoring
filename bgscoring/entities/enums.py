from enum import Enum


class KeyAction(str, Enum):
    VALUE = 'value'
    MATH_OP = 'math_op'


class MathOp(str, Enum):
    MINUS = 'minus'
    PLUS = 'plus'


class PlayerColor(str, Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    YELLOW = 'yellow'
    BLACK = 'black'
