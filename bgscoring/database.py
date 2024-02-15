from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from bgscoring.configs.app_config import DB_ENGINE, DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = (
    f"{DB_ENGINE}://"
    f"{DB_USER}:"
    f"{DB_PASS}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)


class Base(DeclarativeBase):
    pass


metadata = MetaData()


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
