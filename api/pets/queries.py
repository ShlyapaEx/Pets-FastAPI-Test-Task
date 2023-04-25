from sqlalchemy import select, exists, delete
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


async def is_pet_existing(session: AsyncSession, id: int):
    query = select(exists(Pet).where(Pet.id == id))
    pet = await session.execute(query)
    return pet.scalar()


async def delete_many_pets(session: AsyncSession, ids: list[int]):
    query = delete(Pet).where(Pet.id.in_(ids))
    await session.execute(query)
    await session.commit()
