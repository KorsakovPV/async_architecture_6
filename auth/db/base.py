import asyncio
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import app_settings
from core.logs import logger
from db.model import Base, User

engine = create_async_engine(
    url=app_settings.AUTH_DB_DSN,
    pool_pre_ping=True,
    echo=app_settings.SQL_LOGS,
    echo_pool=app_settings.SQL_POOL_LOGS,
)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    engine_postgres = create_async_engine(
        url=app_settings.AUTH_DB_DSN.replace(app_settings.AUTH_DB_NAME, "postgres"),
        pool_pre_ping=True,
        echo=app_settings.SQL_LOGS,
        echo_pool=app_settings.SQL_POOL_LOGS,
    )
    async with engine_postgres.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("create_db_and_tables")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def main():
    await create_db_and_tables()


if __name__ == "__main__":
    asyncio.run(main())
