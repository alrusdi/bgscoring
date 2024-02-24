"""..."""
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.enums import KeyAction
from bgscoring.entities.models.model_key import Key


class KeyDAL:
    """Data Access Layer for operating key info."""

    def __init__(self, db_session: AsyncSession):
        """..."""
        self.db_session = db_session

    async def dal_create_key(
        self,
        value: str,
        display_value: str,
        data_type: Decimal,
        action: KeyAction,
    ) -> Key:
        """..."""
        new_key = Key(
            value=value,
            display_value=display_value,
            data_type=data_type,
            action=action,
        )
        self.db_session.add(new_key)
        await self.db_session.commit()
        return new_key

    async def dal_get_key_by_value(self, value: str) -> Key | None:
        """..."""
        query = select(Key).where(Key.value == value)
        res = await self.db_session.execute(query)
        key_row = res.fetchone()
        if key_row is not None:
            return key_row[0]
        return None

    async def dal_get_key_by_id(self, key_id: UUID) -> Key | None:
        """..."""
        query = select(Key).where(Key.key_id == key_id)
        res = await self.db_session.execute(query)
        key_row = res.fetchone()
        if key_row is not None:
            return key_row[0]
        return None

    async def dal_update_key(self, key_id: UUID, **kwargs) -> Key | None:
        """..."""
        query = (
            update(Key)
            .where(Key.key_id == key_id)
            .values(kwargs)
            .returning(Key)
        )
        res = await self.db_session.execute(query)
        update_key_id_row = res.fetchone()
        if update_key_id_row is not None:
            return update_key_id_row[0]
        return None

    async def dal_delete_key(self, key_id: UUID) -> UUID | None:
        """..."""
        query = (
            update(Key)
            .where(Key.key_id == key_id)
            .returning(Key.key_id)
        )
        res = await self.db_session.execute(query)
        deleted_key_id_row = res.fetchone()
        if deleted_key_id_row is not None:
            return deleted_key_id_row[0]
        return None
