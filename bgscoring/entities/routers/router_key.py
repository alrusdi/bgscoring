from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.database import get_async_session
from bgscoring.entities.crud.crud_key import (
    create_new_key,
    delete_key,
    read_key_by_id,
    read_key_by_value,
    update_key,
)
from bgscoring.entities.schemas.schemas_key import (
    KeyCreate,
    KeyDelete,
    KeyShow,
    KeyUpdate,
)

logger = getLogger(__name__)

key_router = APIRouter(prefix="/key", tags=["key"])


@key_router.post("/create", response_model=KeyShow)
async def create_key(body: KeyCreate, db: AsyncSession = Depends(get_async_session)):
    """..."""
    try:
        return await create_new_key(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@key_router.get("/get_by_id", response_model=KeyShow)
async def get_key_by_id(
    key_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    key = await read_key_by_id(key_id, db)
    if key is None:
        raise HTTPException(
            status_code=404, detail=f"Key with id {key_id} not found."
        )

    return key


@key_router.get("/get_by_title", response_model=KeyShow)
async def get_key_by_value(
    value: str,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    key = await read_key_by_value(value, db)
    if key is None:
        raise HTTPException(
            status_code=404, detail=f"Key with email {value} not found."
        )
    return key


@key_router.patch("/update", response_model=KeyShow)
async def update_key_by_id(
    key_id: UUID,
    body: KeyUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    key_params = body.model_dump(exclude_none=True)
    if key_params == {}:
        raise HTTPException(status_code=422, detail="No one parameters get")
    # this raise is don't work now.
    check_id = await read_key_by_id(key_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Key with id {key_id} not found."
        )

    try:
        updated_key = await update_key(key_params, key_id, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return updated_key


@key_router.delete("/delete", response_model=KeyDelete)
async def delete_key_by_id(
    key_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    check_id = await read_key_by_id(key_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Key with id {key_id} not found."
        )
    deleted_key_id = await delete_key(key_id, db)
    if deleted_key_id is None:
        raise HTTPException(
            status_code=404, detail=f"Key with id {key_id} not found."
        )
    return KeyDelete(deleted_key_id=deleted_key_id)
