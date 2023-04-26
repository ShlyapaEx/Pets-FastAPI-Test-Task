from sqlalchemy import delete, exists, select
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


async def get_existing_pets_ids(session: AsyncSession, ids: list[int]):
    query = select(Pet.id).where(Pet.id.in_(ids))
    pets = await session.execute(query)
    return pets.scalars()


async def delete_many_pets(session: AsyncSession, ids: list[int]):
    query = delete(Pet).where(Pet.id.in_(ids))
    await session.execute(query)
    await session.commit()
