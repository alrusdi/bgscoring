import logging

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from bgscoring.auth.models import User
from bgscoring.auth.utils import get_user_db
from bgscoring.configs.app_config import SECRET_AUTH

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):  # type: ignore
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, _: Request | None = None):
        log.debug("User %s has registered.", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, _: Request | None = None
    ):
        log.debug("User %s has forgot their password. Reset token: %s", user.id, token)

    async def on_after_request_verify(
        self, user: User, token: str, _: Request | None = None
    ):
        log.debug(
            "Verification requested for user %s. Verification token: %s", user.id, token
        )

    async def create(  # type: ignore
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Request | None = None,  # type: ignore
    ) -> models.UP:  # type: ignore
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user  # type: ignore


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
