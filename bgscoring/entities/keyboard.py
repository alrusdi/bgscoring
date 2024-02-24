from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from bgscoring.entities.enums import KeyAction, MathOp


class Key(BaseModel):
    value: str
    display_value: Optional[str] = None
    data_type: Decimal
    action: KeyAction


class Keyboard(BaseModel):
    title: str
    keys: List[Key]


class Cell(BaseModel):
    keyboard: List[Keyboard]
    math_op: MathOp
