"""..."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.dals.dal_cell import CellDAL
from bgscoring.entities.models.model_cell import Cell
from bgscoring.entities.schemas.schemas_cell import CellCreate, CellShow


async def create_new_cell(body: CellCreate, session: AsyncSession) -> CellShow:
    """..."""
    async with session.begin():
        cell_dal = CellDAL(session)
        cell = await cell_dal.dal_create_cell(
            keyboard=body.keyboard,
            math_op=body.math_op,
        )
        return CellShow(
            cell_id=cell.cell_id,
            keyboard=cell.keyboard,
            math_op=cell.math_op,
        )


async def read_cell_by_id(cell_id, session) -> Cell | None:
    """..."""
    async with session.begin():
        cell_dal = CellDAL(session)
        cell = await cell_dal.dal_get_cell_by_id(
            cell_id=cell_id,
        )
        if cell is not None:
            return cell
        return None


async def delete_cell(cell_id, session) -> UUID | None:
    """..."""
    async with session.begin():
        cell_dal = CellDAL(session)
        deleted_cell_id = await cell_dal.dal_delete_cell(
            cell_id=cell_id,
        )
        return deleted_cell_id


async def update_cell(updated_cell_params: dict, cell_id: UUID, session) -> Cell | None:
    """..."""
    async with session.begin():
        cell_dal = CellDAL(session)
        updated_cell = await cell_dal.dal_update_cell(
            cell_id=cell_id, **updated_cell_params
        )
        return updated_cell
