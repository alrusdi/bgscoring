from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.database import get_async_session
from bgscoring.entities.crud.crud_cell import (
    create_new_cell,
    delete_cell,
    read_cell_by_id,
    update_cell,
)
from bgscoring.entities.schemas.schemas_cell import (
    CellCreate,
    CellDelete,
    CellShow,
    CellUpdate,
)

logger = getLogger(__name__)

cell_router = APIRouter(prefix="/cell", tags=["cell"])


@cell_router.post("/create", response_model=CellShow)
async def create_cell(body: CellCreate, db: AsyncSession = Depends(get_async_session)):
    """..."""
    try:
        return await create_new_cell(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@cell_router.get("/get_by_id", response_model=CellShow)
async def get_cell_by_id(
    cell_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    cell = await read_cell_by_id(cell_id, db)
    if cell is None:
        raise HTTPException(
            status_code=404, detail=f"Cell with id {cell_id} not found."
        )

    return cell


@cell_router.patch("/update", response_model=CellShow)
async def update_cell_by_id(
    cell_id: UUID,
    body: CellUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    cell_params = body.model_dump(exclude_none=True)
    if cell_params == {}:
        raise HTTPException(status_code=422, detail="No one parameters get")
    # this raise is don't work now.
    check_id = await read_cell_by_id(cell_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Cell with id {cell_id} not found."
        )

    try:
        updated_cell = await update_cell(cell_params, cell_id, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return updated_cell


@cell_router.delete("/delete", response_model=CellDelete)
async def delete_cell_by_id(
    cell_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """..."""
    check_id = await read_cell_by_id(cell_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"Cell with id {cell_id} not found."
        )
    deleted_cell_id = await delete_cell(cell_id, db)
    if deleted_cell_id is None:
        raise HTTPException(
            status_code=404, detail=f"Cell with id {cell_id} not found."
        )
    return CellDelete(deleted_cell_id=deleted_cell_id)
