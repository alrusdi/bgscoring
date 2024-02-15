from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from bgscoring.auth.manager import get_user_manager
from bgscoring.auth.models import User
from bgscoring.configs.app_config import SECRET_AUTH

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy)  # type: ignore

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])  # type: ignore

current_user = fastapi_users.current_user()
