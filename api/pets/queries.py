from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.pets.models import Pet


async def get_pets(session: AsyncSession, limit: int | None = 20):
    query = select(Pet).limit(limit)
    pets = await session.execute(query)
    return pets.scalars()
