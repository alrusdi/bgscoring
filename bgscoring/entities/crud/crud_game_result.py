"""..."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.dals.dal_game_result import GameResultDAL
from bgscoring.entities.models.model_game_result import GameResult
from bgscoring.entities.schemas.schemas_game_result import GameResultCreate, GameResultShow


async def create_new_game_result(body: GameResultCreate, session: AsyncSession) -> GameResultShow:
    """..."""
    async with session.begin():
        game_result_dal = GameResultDAL(session)
        game_result = await game_result_dal.dal_create_game_result(
            game=body.game,
            created_at=body.created_at,
            author=body.author,
            session_id=body.session_id,
            players=body.players,
        )
        return GameResultShow(
            game_result_id=game_result.game_result_id,
            game=game_result.game,
            created_at=game_result.created_at,
            author=game_result.author,
            session_id=game_result.session_id,
            players=game_result.players,
        )


async def read_game_result_by_id(game_result_id, session) -> GameResult | None:
    """..."""
    async with session.begin():
        game_result_dal = GameResultDAL(session)
        game_result = await game_result_dal.dal_get_game_result_by_id(
            game_result_id=game_result_id,
        )
        if game_result is not None:
            return game_result
        return None


async def delete_game_result(game_result_id, session) -> UUID | None:
    """..."""
    async with session.begin():
        game_result_dal = GameResultDAL(session)
        deleted_game_result_id = await game_result_dal.dal_delete_game_result(
            game_result_id=game_result_id,
        )
        return deleted_game_result_id


async def update_game_result(updated_game_result_params: dict, game_result_id: UUID, session) -> GameResult | None:
    """..."""
    async with session.begin():
        game_result_dal = GameResultDAL(session)
        updated_game_result = await game_result_dal.dal_update_game_result(
            game_result_id=game_result_id, **updated_game_result_params
        )
        return updated_game_result
