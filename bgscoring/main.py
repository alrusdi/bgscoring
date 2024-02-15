from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from bgscoring.auth.base_config import auth_backend
from bgscoring.auth.manager import get_user_manager
from bgscoring.auth.models import User
from bgscoring.auth.schemas import UserCreate, UserRead
from bgscoring.configs.app_config import REDIS_HOST, REDIS_PORT
from bgscoring.games.router import router as router_games

app = FastAPI(
    title='Board Games Scoring'
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])  # type: ignore

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_games)

@app.get("/ping")
async def ping():
    return {"ping": "pong"}

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@asynccontextmanager
async def lifespan(*_):
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi_cache')
