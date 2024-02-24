import uuid
from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field

from bgscoring.entities.enums import PlayerColor


class GamePlayerCreate(BaseModel):
    color: PlayerColor
    name: Optional[str]
    values: Decimal


class GamePlayerShow(BaseModel):
    game_player_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    color: PlayerColor
    name: Optional[str]
    values: Decimal


class GamePlayerUpdate(BaseModel):
    color: Optional[PlayerColor]
    name: Optional[str]
    values: Optional[Decimal]


class GamePlayerDelete(BaseModel):
    deleted_game_player_id: UUID4

