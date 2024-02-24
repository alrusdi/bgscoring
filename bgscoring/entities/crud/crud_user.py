"""..."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.auth.hasher import Hasher
from bgscoring.entities.dals.dal_user import UserDAL
from bgscoring.entities.models.model_user import User
from bgscoring.entities.schemas.schemas_user import UserCreate, UserShow


async def create_new_user(body: UserCreate, session: AsyncSession) -> UserShow:
    """..."""
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.dal_create_user(
            username=body.username,
            email=body.email,
            password=Hasher.hash_password(body.password),
        )
        return UserShow(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            hashed_password=user.hashed_password,
        )


async def read_user_by_email(email: str, session: AsyncSession) -> User | None:
    """..."""
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.dal_get_user_by_email(email)
        if user is not None:
            return user
        return None


async def read_user_by_id(user_id, session) -> User | None:
    """..."""
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.dal_get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return user
        return None


async def delete_user(user_id, session) -> UUID | None:
    """..."""
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.dal_delete_user(
            user_id=user_id,
        )
        return deleted_user_id


async def update_user(updated_user_params: dict, user_id: UUID, session) -> User | None:
    """..."""
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user = await user_dal.dal_update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user
