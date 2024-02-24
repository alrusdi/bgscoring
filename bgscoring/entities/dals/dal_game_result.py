"""..."""
import datetime
from typing import List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.models.model_game_result import GameResult
from bgscoring.entities.schemas.schemas_game import GameShow
from bgscoring.entities.schemas.schemas_game_player import GamePlayerShow
from bgscoring.entities.schemas.schemas_user import UserShow


class GameResultDAL:
    """Data Access Layer for operating GameResult info."""

    def __init__(self, db_session: AsyncSession):
        """..."""
        self.db_session = db_session

    async def dal_create_game_result(
        self,
        game: GameShow,
        created_at: datetime.datetime,
        author: UserShow,
        session_id: str,
        players: List[GamePlayerShow],
    ) -> GameResult:
        """..."""
        new_game_result = GameResult(
            game=game,
            created_at=created_at,
            author=author,
            session_id=session_id,
            players=players,
        )
        self.db_session.add(new_game_result)
        await self.db_session.commit()
        return new_game_result

    async def dal_get_game_result_by_id(self, game_result_id: UUID) -> GameResult | None:
        """..."""
        query = select(GameResult).where(GameResult.game_result_id == game_result_id)
        res = await self.db_session.execute(query)
        game_result_row = res.fetchone()
        if game_result_row is not None:
            return game_result_row[0]
        return None

    async def dal_update_game_result(self, game_result_id: UUID, **kwargs) -> GameResult | None:
        """..."""
        query = (
            update(GameResult)
            .where(GameResult.game_result_id == game_result_id)
            .values(kwargs)
            .returning(GameResult)
        )
        res = await self.db_session.execute(query)
        update_game_result_id_row = res.fetchone()
        if update_game_result_id_row is not None:
            return update_game_result_id_row[0]
        return None

    async def dal_delete_game_result(self, game_result_id: UUID) -> UUID | None:
        """..."""
        query = (
            update(GameResult)
            .where(GameResult.game_result_id == game_result_id)
            .values(is_active=False)
            .returning(GameResult.game_result_id)
        )
        res = await self.db_session.execute(query)
        deleted_game_result_id_row = res.fetchone()
        if deleted_game_result_id_row is not None:
            return deleted_game_result_id_row[0]
        return None
