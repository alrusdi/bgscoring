"""..."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.dals.dal_game_player import GamePlayerDAL
from bgscoring.entities.models.model_game_player import GamePlayer
from bgscoring.entities.schemas.schemas_game_player import GamePlayerCreate, GamePlayerShow


async def create_new_game_player(body: GamePlayerCreate, session: AsyncSession) -> GamePlayerShow:
    """..."""
    async with session.begin():
        game_player_dal = GamePlayerDAL(session)
        game_player = await game_player_dal.dal_create_game_player(
            color=body.color,
            name=body.name,
            values=body.values,
        )
        return GamePlayerShow(
            game_player_id=game_player.game_player_id,
            color=game_player.color,
            name=game_player.name,
            values=game_player.values,
        )


async def read_game_player_by_color(color: str, session: AsyncSession) -> GamePlayer | None:
    """..."""
    async with session.begin():
        game_player_dal = GamePlayerDAL(session)
        game_player = await game_player_dal.dal_get_game_player_by_color(color)
        if game_player is not None:
            return game_player
        return None


async def read_game_player_by_id(game_player_id, session) -> GamePlayer | None:
    """..."""
    async with session.begin():
        game_player_dal = GamePlayerDAL(session)
        game_player = await game_player_dal.dal_get_game_player_by_id(
            game_player_id=game_player_id,
        )
        if game_player is not None:
            return game_player
        return None


async def delete_game_player(game_player_id, session) -> UUID | None:
    """..."""
    async with session.begin():
        game_player_dal = GamePlayerDAL(session)
        deleted_game_player_id = await game_player_dal.dal_delete_game_player(
            game_player_id=game_player_id,
        )
        return deleted_game_player_id


async def update_game_player(updated_game_player_params: dict, game_player_id: UUID, session) -> GamePlayer | None:
    """..."""
    async with session.begin():
        game_player_dal = GamePlayerDAL(session)
        updated_game_player = await game_player_dal.dal_update_game_player(
            game_player_id=game_player_id, **updated_game_player_params
        )
        return updated_game_player
