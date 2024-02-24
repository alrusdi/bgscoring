"""..."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.dals.dal_key import KeyDAL
from bgscoring.entities.models.model_key import Key
from bgscoring.entities.schemas.schemas_key import KeyCreate, KeyShow


async def create_new_key(body: KeyCreate, session: AsyncSession) -> KeyShow:
    """..."""
    async with session.begin():
        key_dal = KeyDAL(session)
        key = await key_dal.dal_create_key(
            value=body.value,
            display_value=body.display_value,
            data_type=body.data_type,
            action=body.action,
        )
        return KeyShow(
            key_id=key.key_id,
            value=key.value,
            display_value=key.display_value,
            data_type=key.data_type,
            action=key.action,
        )


async def read_key_by_value(value: str, session: AsyncSession) -> Key | None:
    """..."""
    async with session.begin():
        key_dal = KeyDAL(session)
        key = await key_dal.dal_get_key_by_value(value)
        if key is not None:
            return key
        return None


async def read_key_by_id(key_id, session) -> Key | None:
    """..."""
    async with session.begin():
        key_dal = KeyDAL(session)
        key = await key_dal.dal_get_key_by_id(
            key_id=key_id,
        )
        if key is not None:
            return key
        return None


async def delete_key(key_id, session) -> UUID | None:
    """..."""
    async with session.begin():
        key_dal = KeyDAL(session)
        deleted_key_id = await key_dal.dal_delete_key(
            key_id=key_id,
        )
        return deleted_key_id


async def update_key(updated_key_params: dict, key_id: UUID, session) -> Key | None:
    """..."""
    async with session.begin():
        key_dal = KeyDAL(session)
        updated_key = await key_dal.dal_update_key(
            key_id=key_id, **updated_key_params
        )
        return updated_key
