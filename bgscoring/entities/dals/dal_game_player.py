"""..."""
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.enums import PlayerColor
from bgscoring.entities.models.model_game_player import GamePlayer


class GamePlayerDAL:
    """Data Access Layer for operating GamePlayer info."""

    def __init__(self, db_session: AsyncSession):
        """..."""
        self.db_session = db_session

    async def dal_create_game_player(
        self,
        color: PlayerColor,
        name: str,
        values: Decimal,
    ) -> GamePlayer:
        """..."""
        new_game_player = GamePlayer(
            color=color,
            name=name,
            values=values,
        )
        self.db_session.add(new_game_player)
        await self.db_session.commit()
        return new_game_player

    async def dal_get_game_player_by_color(self, color: str) -> GamePlayer | None:
        """..."""
        query = select(GamePlayer).where(GamePlayer.color == color)
        res = await self.db_session.execute(query)
        game_player_row = res.fetchone()
        if game_player_row is not None:
            return game_player_row[0]
        return None

    async def dal_get_game_player_by_id(self, game_player_id: UUID) -> GamePlayer | None:
        """..."""
        query = select(GamePlayer).where(GamePlayer.game_player_id == game_player_id)
        res = await self.db_session.execute(query)
        game_player_row = res.fetchone()
        if game_player_row is not None:
            return game_player_row[0]
        return None

    async def dal_update_game_player(self, game_player_id: UUID, **kwargs) -> GamePlayer | None:
        """..."""
        query = (
            update(GamePlayer)
            .where(GamePlayer.game_player_id == game_player_id)
            .values(kwargs)
            .returning(GamePlayer)
        )
        res = await self.db_session.execute(query)
        update_game_player_id_row = res.fetchone()
        if update_game_player_id_row is not None:
            return update_game_player_id_row[0]
        return None

    async def dal_delete_game_player(self, game_player_id: UUID) -> UUID | None:
        """..."""
        query = (
            update(GamePlayer)
            .where(GamePlayer.game_player_id == game_player_id)
            .values(is_active=False)
            .returning(GamePlayer.game_player_id)
        )
        res = await self.db_session.execute(query)
        deleted_game_player_id_row = res.fetchone()
        if deleted_game_player_id_row is not None:
            return deleted_game_player_id_row[0]
        return None
