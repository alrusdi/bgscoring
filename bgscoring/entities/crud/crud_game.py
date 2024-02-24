"""..."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.dals.dal_game import GameDAL
from bgscoring.entities.models.model_game import Game
from bgscoring.entities.schemas.schemas_game import GameCreate, GameShow


async def create_new_game(body: GameCreate, session: AsyncSession) -> GameShow:
    """..."""
    async with session.begin():
        game_dal = GameDAL(session)
        game = await game_dal.dal_create_game(
            title=body.title,
            cells=body.cells,
        )
        return GameShow(
            game_id=game.game_id,
            title=game.title,
            cells=game.cells,
        )


async def read_game_by_title(title: str, session: AsyncSession) -> Game | None:
    """..."""
    async with session.begin():
        game_dal = GameDAL(session)
        game = await game_dal.dal_get_game_by_title(title)
        if game is not None:
            return game
        return None


async def read_game_by_id(game_id, session) -> Game | None:
    """..."""
    async with session.begin():
        game_dal = GameDAL(session)
        game = await game_dal.dal_get_game_by_id(
            game_id=game_id,
        )
        if game is not None:
            return game
        return None


async def delete_game(game_id, session) -> UUID | None:
    """..."""
    async with session.begin():
        game_dal = GameDAL(session)
        deleted_game_id = await game_dal.dal_delete_game(
            game_id=game_id,
        )
        return deleted_game_id


async def update_game(updated_game_params: dict, game_id: UUID, session) -> Game | None:
    """..."""
    async with session.begin():
        game_dal = GameDAL(session)
        updated_game = await game_dal.dal_update_game(
            game_id=game_id, **updated_game_params
        )
        return updated_game
