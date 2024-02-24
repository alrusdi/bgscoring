import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from bgscoring.entities.enums import PlayerColor
from bgscoring.entities.keyboard import Cell
from bgscoring.entities.user import User


class Game(BaseModel):
    title: str
    cells: List[Cell]


class GamePlayer(BaseModel):
    color: PlayerColor
    name: Optional[str]
    values: Decimal
    user: Optional[User]


class GameResult(BaseModel):
    game: Game
    created_at: datetime.datetime
    author: Optional[User]
    session_id: Optional[str]
    players: List['GamePlayer']
