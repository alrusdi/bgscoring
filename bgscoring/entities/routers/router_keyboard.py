from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.database import get_async_session
from bgscoring.entities.crud.crud_keyboard import (
    create_new_keyboard,
    delete_keyboard,
    read_keyboard_by_id,
    read_keyboard_by_title,
    update_keyboard,
)
from bgscoring.entities.schemas.schemas_keyboard import (
    KeyboardCreate,
    KeyboardDelete,
    KeyboardShow,
    KeyboardUpdate,
)

logger = getLogger(__name__)

keyboard_router = APIRouter(prefix="/keyboard", tags=["keyboard"])


@keyboard_router.post("/create", response_model=KeyboardShow)
async def create_keyboard(body: KeyboardCreate, db: AsyncSession = Depends(get_async_session)):
    """..."""
    try:
        return await create_new_keyboard(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@keyboard_router.get("/get_by_id", response_model=KeyboardShow)
async def get_keyboard_by_id(
    keyboard_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    keyboard = await read_keyboard_by_id(keyboard_id, db)
    if keyboard is None:
        raise HTTPException(
            status_code=404, detail=f"Keyboard with id {keyboard_id} not found."
        )

    return keyboard


@keyboard_router.get("/get_by_title", response_model=KeyboardShow)
async def get_keyboard_by_title(
    title: str,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    keyboard = await read_keyboard_by_title(title, db)
    if keyboard is None:
        raise HTTPException(
            status_code=404, detail=f"Keyboard with title {title} not found."
        )
    return keyboard


@keyboard_router.patch("/update", response_model=KeyboardShow)
async def update_keyboard_by_id(
    keyboard_id: UUID,
    body: KeyboardUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    keyboard_params = body.model_dump(exclude_none=True)
    if keyboard_params == {}:
        raise HTTPException(status_code=422, detail="No one parameters get")
    # this raise is don't work now.
    check_id = await read_keyboard_by_id(keyboard_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Keyboard with id {keyboard_id} not found."
        )

    try:
        updated_keyboard = await update_keyboard(keyboard_params, keyboard_id, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return updated_keyboard


@keyboard_router.delete("/delete", response_model=KeyboardDelete)
async def delete_keyboard_by_id(
    keyboard_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    check_id = await read_keyboard_by_id(keyboard_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Keyboard with id {keyboard_id} not found."
        )
    deleted_keyboard_id = await delete_keyboard(keyboard_id, db)
    if deleted_keyboard_id is None:
        raise HTTPException(
            status_code=404, detail=f"Keyboard with id {keyboard_id} not found."
        )
    return KeyboardDelete(deleted_keyboard_id=deleted_keyboard_id)
