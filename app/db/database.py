import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_USER, DB_PASSWORD, DB_NAME, DB_SERVER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession)

Base = declarative_base()


async def get_db_session() -> AsyncSession:
    """
    The get_db_session function is a dependency for getting an async session.
    It uses the async_session context manager to create a new session, and then yields it.

    :return: An AsyncSession object
    """
    async with async_session() as session:
        yield session
