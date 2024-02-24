from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.database import get_async_session
from bgscoring.entities.crud.crud_game import (
    create_new_game,
    delete_game,
    read_game_by_id,
    read_game_by_title,
    update_game,
)
from bgscoring.entities.schemas.schemas_game import (
    GameCreate,
    GameDelete,
    GameShow,
    GameUpdate,
)

logger = getLogger(__name__)

game_router = APIRouter(prefix="/game", tags=["game"])


@game_router.post("/create", response_model=GameShow)
async def create_game(body: GameCreate, db: AsyncSession = Depends(get_async_session)):
    """..."""
    try:
        return await create_new_game(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@game_router.get("/get_by_id", response_model=GameShow)
async def get_game_by_id(
    game_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    game = await read_game_by_id(game_id, db)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f"Game with id {game_id} not found."
        )

    return game


@game_router.get("/get_by_title", response_model=GameShow)
async def get_game_by_title(
    title: str,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    game = await read_game_by_title(title, db)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f"Game with title {title} not found."
        )
    return game


@game_router.patch("/update", response_model=GameShow)
async def update_game_by_id(
    game_id: UUID,
    body: GameUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    game_params = body.model_dump(exclude_none=True)
    if game_params == {}:
        raise HTTPException(status_code=422, detail="No one parameters get")
    # this raise is don't work now.
    check_id = await read_game_by_id(game_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Game with id {game_id} not found."
        )

    try:
        updated_game = await update_game(game_params, game_id, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return updated_game


@game_router.delete("/delete", response_model=GameDelete)
async def delete_game_by_id(
    game_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    check_id = await read_game_by_id(game_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Game with id {game_id} not found."
        )
    deleted_game_id = await delete_game(game_id, db)
    if deleted_game_id is None:
        raise HTTPException(
            status_code=404, detail=f"Game with id {game_id} not found."
        )
    return GameDelete(deleted_game_id=deleted_game_id)
