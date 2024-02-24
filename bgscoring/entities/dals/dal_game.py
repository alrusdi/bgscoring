"""..."""
from typing import List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.models.model_game import Game
from bgscoring.entities.schemas.schemas_cell import CellShow


class GameDAL:
    """Data Access Layer for operating Game info."""

    def __init__(self, db_session: AsyncSession):
        """..."""
        self.db_session = db_session

    async def dal_create_game(
        self,
        title: str,
        cells: List[CellShow]
    ) -> Game:
        """..."""
        new_game = Game(
            title=title,
            cells=cells,
        )
        self.db_session.add(new_game)
        await self.db_session.commit()
        return new_game

    async def dal_get_game_by_title(self, title: str) -> Game | None:
        """..."""
        query = select(Game).where(Game.title == title)
        res = await self.db_session.execute(query)
        game_row = res.fetchone()
        if game_row is not None:
            return game_row[0]
        return None

    async def dal_get_game_by_id(self, game_id: UUID) -> Game | None:
        """..."""
        query = select(Game).where(Game.game_id == game_id)
        res = await self.db_session.execute(query)
        game_row = res.fetchone()
        if game_row is not None:
            return game_row[0]
        return None

    async def dal_update_game(self, game_id: UUID, **kwargs) -> Game | None:
        """..."""
        query = (
            update(Game)
            .where(Game.game_id == game_id)
            .values(kwargs)
            .returning(Game)
        )
        res = await self.db_session.execute(query)
        update_game_id_row = res.fetchone()
        if update_game_id_row is not None:
            return update_game_id_row[0]
        return None

    async def dal_delete_game(self, game_id: UUID) -> UUID | None:
        """..."""
        query = (
            update(Game)
            .where(Game.game_id == game_id)
            .values(is_active=False)
            .returning(Game.game_id)
        )
        res = await self.db_session.execute(query)
        deleted_game_id_row = res.fetchone()
        if deleted_game_id_row is not None:
            return deleted_game_id_row[0]
        return None
