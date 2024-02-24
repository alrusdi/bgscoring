from typing import List

from pydantic import UUID4, BaseModel

from bgscoring.entities.enums import MathOp
from bgscoring.entities.schemas.schemas_keyboard import KeyboardShow


class CellShow(BaseModel):
    keyboard: List[KeyboardShow]
    math_op: MathOp


class CellCreate(BaseModel):
    keyboard: List[KeyboardShow]
    math_op: MathOp


class CellUpdate(BaseModel):
    keyboard: List[KeyboardShow]
    math_op: MathOp


class CellDelete(BaseModel):
    deleted_cell_id: UUID4
