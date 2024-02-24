"""..."""
from typing import List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.enums import MathOp
from bgscoring.entities.models.model_cell import Cell
from bgscoring.entities.models.model_keyboard import Keyboard


class CellDAL:
    """Data Access Layer for operating cell info."""

    def __init__(self, db_session: AsyncSession):
        """..."""
        self.db_session = db_session

    async def dal_create_cell(
        self,
        keyboard: List[Keyboard],
        math_op: MathOp,
    ) -> Cell:
        """..."""
        new_cell = Cell(
            keyboard=keyboard,
            math_op=math_op,
        )
        self.db_session.add(new_cell)
        await self.db_session.commit()
        return new_cell

    async def dal_get_cell_by_id(self, cell_id: UUID) -> Cell | None:
        """..."""
        query = select(Cell).where(Cell.cell_id == cell_id)
        res = await self.db_session.execute(query)
        cell_row = res.fetchone()
        if cell_row is not None:
            return cell_row[0]
        return None

    async def dal_update_cell(self, cell_id: UUID, **kwargs) -> Cell | None:
        """..."""
        query = (
            update(Cell)
            .where(Cell.cell_id == cell_id)
            .values(kwargs)
            .returning(Cell)
        )
        res = await self.db_session.execute(query)
        update_cell_id_row = res.fetchone()
        if update_cell_id_row is not None:
            return update_cell_id_row[0]
        return None

    async def dal_delete_cell(self, cell_id: UUID) -> UUID | None:
        """..."""
        query = (
            update(Cell)
            .where(Cell.cell_id == cell_id)
            .returning(Cell.cell_id)
        )
        res = await self.db_session.execute(query)
        deleted_cell_id_row = res.fetchone()
        if deleted_cell_id_row is not None:
            return deleted_cell_id_row[0]
        return None
