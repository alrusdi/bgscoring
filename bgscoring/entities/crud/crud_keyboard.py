"""..."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.entities.dals.dal_keyboard import KeyboardDAL
from bgscoring.entities.models.model_keyboard import Keyboard
from bgscoring.entities.schemas.schemas_keyboard import KeyboardCreate, KeyboardShow


async def create_new_keyboard(body: KeyboardCreate, session: AsyncSession) -> KeyboardShow:
    """..."""
    async with session.begin():
        keyboard_dal = KeyboardDAL(session)
        keyboard = await keyboard_dal.dal_create_keyboard(
            title=body.title,
            keys=body.keys,
        )
        return KeyboardShow(
            keyboard_id=keyboard.keyboard_id,
            title=keyboard.title,
            keys=keyboard.keys,
        )


async def read_keyboard_by_title(title: str, session: AsyncSession) -> Keyboard | None:
    """..."""
    async with session.begin():
        keyboard_dal = KeyboardDAL(session)
        keyboard = await keyboard_dal.dal_get_keyboard_by_title(title)
        if keyboard is not None:
            return keyboard
        return None


async def read_keyboard_by_id(keyboard_id, session) -> Keyboard | None:
    """..."""
    async with session.begin():
        keyboard_dal = KeyboardDAL(session)
        keyboard = await keyboard_dal.dal_get_keyboard_by_id(
            keyboard_id=keyboard_id,
        )
        if keyboard is not None:
            return keyboard
        return None


async def delete_keyboard(keyboard_id, session) -> UUID | None:
    """..."""
    async with session.begin():
        keyboard_dal = KeyboardDAL(session)
        deleted_keyboard_id = await keyboard_dal.dal_delete_keyboard(
            keyboard_id=keyboard_id,
        )
        return deleted_keyboard_id


async def update_keyboard(updated_keyboard_params: dict, keyboard_id: UUID, session) -> Keyboard | None:
    """..."""
    async with session.begin():
        keyboard_dal = KeyboardDAL(session)
        updated_keyboard = await keyboard_dal.dal_update_keyboard(
            keyboard_id=keyboard_id, **updated_keyboard_params
        )
        return updated_keyboard
