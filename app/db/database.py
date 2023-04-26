import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_user = os.getenv('POSTGRES_USER', 'postgres')
db_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
db_server = os.getenv('POSTGRES_SERVER', 'localhost')
db_name = os.getenv('POSTGRES_DB', 'fastapi_pets_db')

DATABASE_URL = f'postgresql+asyncpg://{db_user}:{db_password}@{db_server}/{db_name}'

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
