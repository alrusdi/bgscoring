from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from bgscoring.configs.app_config import REDIS_HOST, REDIS_PORT
from bgscoring.entities.routers.router_cell import cell_router
from bgscoring.entities.routers.router_game import game_router
from bgscoring.entities.routers.router_game_players import game_player_router
from bgscoring.entities.routers.router_game_result import game_result_router
from bgscoring.entities.routers.router_key import key_router
from bgscoring.entities.routers.router_keyboard import keyboard_router
from bgscoring.entities.routers.router_user import user_router


@asynccontextmanager
async def lifespan(*_):
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix='bgscoring_cache')
    yield


app = FastAPI(
    title="Board Games Scoring",
    lifespan=lifespan,
)

app.include_router(user_router)
app.include_router(key_router)
app.include_router(keyboard_router)
app.include_router(cell_router)
app.include_router(game_router)
app.include_router(game_player_router)
app.include_router(game_result_router)


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
