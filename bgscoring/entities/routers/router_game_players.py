from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.database import get_async_session
from bgscoring.entities.crud.crud_game_players import (
    create_new_game_player,
    delete_game_player,
    read_game_player_by_color,
    read_game_player_by_id,
    update_game_player,
)
from bgscoring.entities.schemas.schemas_game_player import (
    GamePlayerCreate,
    GamePlayerDelete,
    GamePlayerShow,
    GamePlayerUpdate,
)

logger = getLogger(__name__)

game_player_router = APIRouter(prefix="/game_player", tags=["game_player"])


@game_player_router.post("/create", response_model=GamePlayerShow)
async def create_game_player(body: GamePlayerCreate, db: AsyncSession = Depends(get_async_session)):
    """..."""
    try:
        return await create_new_game_player(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@game_player_router.get("/get_by_id", response_model=GamePlayerShow)
async def get_game_player_by_id(
    game_player_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    game_player = await read_game_player_by_id(game_player_id, db)
    if game_player is None:
        raise HTTPException(
            status_code=404, detail=f"GamePlayer with id {game_player_id} not found."
        )

    return game_player


@game_player_router.get("/get_by_color", response_model=GamePlayerShow)
async def get_game_player_by_color(
    color: str,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    game_player = await read_game_player_by_color(color, db)
    if game_player is None:
        raise HTTPException(
            status_code=404, detail=f"GamePlayer with color {color} not found."
        )
    return game_player


@game_player_router.patch("/update", response_model=GamePlayerShow)
async def update_game_player_by_id(
    game_player_id: UUID,
    body: GamePlayerUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    game_player_params = body.model_dump(exclude_none=True)
    if game_player_params == {}:
        raise HTTPException(status_code=422, detail="No one parameters get")
    # this raise is don't work now.
    check_id = await read_game_player_by_id(game_player_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"GamePlayer with id {game_player_id} not found."
        )

    try:
        updated_game_player = await update_game_player(game_player_params, game_player_id, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return updated_game_player


@game_player_router.delete("/delete", response_model=GamePlayerDelete)
async def delete_game_player_by_id(
    game_player_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    check_id = await read_game_player_by_id(game_player_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"GamePlayer with id {game_player_id} not found."
        )
    deleted_game_player_id = await delete_game_player(game_player_id, db)
    if deleted_game_player_id is None:
        raise HTTPException(
            status_code=404, detail=f"GamePlayer with id {game_player_id} not found."
        )
    return GamePlayerDelete(deleted_game_player_id=deleted_game_player_id)
