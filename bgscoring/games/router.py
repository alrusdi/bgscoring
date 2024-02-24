import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bgscoring.database import get_async_session
from bgscoring.games.models import Game
from bgscoring.games.schemas import GamesCreate

router = APIRouter(
    prefix="/game",
    tags=["Game"]
)


@router.get("/")
async def get_specific_game(game_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Game).where(Game.id == game_id)
        result = await session.execute(query)
        games_list = [dict(game) for game in result.all()]
        return games_list
    except Exception:
        raise HTTPException(status_code=505, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.get("/redis-test")
@cache(expire=30)
def get_redis_test():
    time.sleep(2)
    return "Data"


@router.post("/")
async def add_specific_games(new_game: GamesCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Game).values(**new_game.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            'status': 'success'
        }
    except Exception:
        return {
            'status': 'error',
            'data': None,
            'details': None
        }
