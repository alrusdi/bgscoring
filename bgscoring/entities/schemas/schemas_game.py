import uuid
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from bgscoring.entities.schemas.schemas_cell import CellShow


class GameCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255, default=None)
    cells: List[CellShow]


class GameShow(BaseModel):
    game_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    cells: List[CellShow]


class GameUpdate(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=255, default=None)
    cells: List[CellShow]


class GameDelete(BaseModel):
    deleted_game_id: UUID4

