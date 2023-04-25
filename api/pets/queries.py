from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.pets.models import Pet
from api.pets.schemas import PetCreateSchema


async def get_pets(session: AsyncSession, limit: int | None = 20):
    query = select(Pet).limit(limit)
    pets = await session.execute(query)
    return pets.scalars()


async def create_new_pet(session: AsyncSession, pet: PetCreateSchema):
    new_pet = Pet(name=pet.name, age=pet.age, type=pet.type)
    session.add(new_pet)
    await session.commit()
    await session.refresh(new_pet)
    return new_pet
