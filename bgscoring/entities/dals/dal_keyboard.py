"""..."""
from typing import List
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.models.model_keyboard import Keyboard
from bgscoring.entities.schemas.schemas_key import KeyShow


class KeyboardDAL:
    """Data Access Layer for operating keyboard info."""

    def __init__(self, db_session: AsyncSession):
        """..."""
        self.db_session = db_session

    async def dal_create_keyboard(
        self,
        title: str,
        keys: List[KeyShow],
    ) -> Keyboard:
        """..."""
        new_keyboard = Keyboard(
            title=title,
            keys=keys,
        )
        self.db_session.add(new_keyboard)
        await self.db_session.commit()
        return new_keyboard

    async def dal_get_keyboard_by_title(self, title: str) -> Keyboard | None:
        """..."""
        query = select(Keyboard).where(Keyboard.title == title)
        res = await self.db_session.execute(query)
        keyboard_row = res.fetchone()
        if keyboard_row is not None:
            return keyboard_row[0]
        return None

    async def dal_get_keyboard_by_id(self, keyboard_id: UUID) -> Keyboard | None:
        """..."""
        query = select(Keyboard).where(Keyboard.keyboard_id == keyboard_id)
        res = await self.db_session.execute(query)
        keyboard_row = res.fetchone()
        if keyboard_row is not None:
            return keyboard_row[0]
        return None

    async def dal_update_keyboard(self, keyboard_id: UUID, **kwargs) -> Keyboard | None:
        """..."""
        query = (
            update(Keyboard)
            .where(Keyboard.keyboard_id == keyboard_id)
            .values(kwargs)
            .returning(Keyboard)
        )
        res = await self.db_session.execute(query)
        update_keyboard_id_row = res.fetchone()
        if update_keyboard_id_row is not None:
            return update_keyboard_id_row[0]
        return None

    async def dal_delete_keyboard(self, keyboard_id: UUID) -> UUID | None:
        """..."""
        query = (
            update(Keyboard)
            .where(Keyboard.keyboard_id == keyboard_id)
            .returning(Keyboard.keyboard_id)
        )
        res = await self.db_session.execute(query)
        deleted_keyboard_id_row = res.fetchone()
        if deleted_keyboard_id_row is not None:
            return deleted_keyboard_id_row[0]
        return None
