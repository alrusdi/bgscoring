from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.database import get_async_session
from bgscoring.entities.crud.crud_game_result import (
    create_new_game_result,
    delete_game_result,
    read_game_result_by_id,
    update_game_result,
)
from bgscoring.entities.schemas.schemas_game_result import (
    GameResultCreate,
    GameResultDelete,
    GameResultShow,
    GameResultUpdate,
)

logger = getLogger(__name__)

game_result_router = APIRouter(prefix="/game_result", tags=["game_result"])


@game_result_router.post("/create", response_model=GameResultShow)
async def create_game_result(body: GameResultCreate, db: AsyncSession = Depends(get_async_session)):
    """..."""
    try:
        return await create_new_game_result(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@game_result_router.get("/get_by_id", response_model=GameResultShow)
async def get_game_result_by_id(
    game_result_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    game_result = await read_game_result_by_id(game_result_id, db)
    if game_result is None:
        raise HTTPException(
            status_code=404, detail=f"GameResult with id {game_result_id} not found."
        )

    return game_result


@game_result_router.patch("/update", response_model=GameResultShow)
async def update_game_result_by_id(
    game_result_id: UUID,
    body: GameResultUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    game_result_params = body.model_dump(exclude_none=True)
    if game_result_params == {}:
        raise HTTPException(status_code=422, detail="No one parameters get")
    # this raise is don't work now.
    check_id = await read_game_result_by_id(game_result_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"GameResult with id {game_result_id} not found."
        )

    try:
        updated_game_result = await update_game_result(game_result_params, game_result_id, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return updated_game_result


@game_result_router.delete("/delete", response_model=GameResultDelete)
async def delete_game_result_by_id(
    game_result_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    check_id = await read_game_result_by_id(game_result_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"GameResult with id {game_result_id} not found."
        )
    deleted_game_result_id = await delete_game_result(game_result_id, db)
    if deleted_game_result_id is None:
        raise HTTPException(
            status_code=404, detail=f"GameResult with id {game_result_id} not found."
        )
    return GameResultDelete(deleted_game_result_id=deleted_game_result_id)
