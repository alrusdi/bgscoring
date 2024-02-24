import datetime
import uuid
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field

from bgscoring.entities.schemas.schemas_game import GameShow
from bgscoring.entities.schemas.schemas_game_player import GamePlayerShow
from bgscoring.entities.schemas.schemas_user import UserShow


class GameResultCreate(BaseModel):
    game: GameShow
    created_at: datetime.datetime
    author: Optional[UserShow]
    session_id: Optional[str]
    players: List[GamePlayerShow]


class GameResultShow(BaseModel):
    game_result_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    game: GameShow
    created_at: datetime.datetime
    author: Optional[UserShow]
    session_id: Optional[str]
    players: List[GamePlayerShow]


class GameResultUpdate(BaseModel):
    game: Optional[GameShow]
    author: Optional[UserShow]
    session_id: Optional[str]
    players: Optional[List[GamePlayerShow]]


class GameResultDelete(BaseModel):
    deleted_game_result_id: UUID4

