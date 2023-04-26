from sqlalchemy import ScalarResult, delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.pets.models import Pet
from api.pets.schemas import PetCreateSchema


async def get_pets(session: AsyncSession, limit: int | None = 20) -> ScalarResult[Pet]:
    """
    The get_pets function returns a list of pets from database as ScalarResult.

    :param session: AsyncSession: SQLAlchemy AsyncSession object
    :param limit: int | None: Limit the number of pets returned
    :return: A list of pet objects
    """
    query = select(Pet).limit(limit)
    pets = await session.execute(query)
    return pets.scalars()


async def create_new_pet(session: AsyncSession, pet: PetCreateSchema) -> Pet:
    """
    The create_new_pet function creates a new pet in the database.

    :param session: AsyncSession: SQLAlchemy AsyncSession object
    :param pet: PetCreateSchema: New verified pet data
    :return: A Pet object
    """
    new_pet = Pet(name=pet.name, age=pet.age, type=pet.type)
    session.add(new_pet)
    await session.commit()
    await session.refresh(new_pet)
    return new_pet


async def get_existing_pets_ids(session: AsyncSession, ids: list[int]) -> ScalarResult[int]:
    """
    The get_existing_pets_ids function takes a list of pet ids
    and returns the subset of those ids that are already in the database.

    :param session: AsyncSession: SQLAlchemy AsyncSession object
    :param ids: list[int]: list of pet ids to search in database
    :return: A list of existing pets ids
    """
    query = select(Pet.id).where(Pet.id.in_(ids))
    pets = await session.execute(query)
    return pets.scalars()


async def delete_many_pets(session: AsyncSession, ids: list[int]) -> None:
    """
    The delete_many_pets function deletes many pets from the database.

    :param session: AsyncSession: SQLAlchemy AsyncSession object
    :param ids: list[int]: The ids of the pets to be deleted from database
    :return: None
    """
    query = delete(Pet).where(Pet.id.in_(ids))
    await session.execute(query)
    await session.commit()


async def is_pet_in_db(session: AsyncSession, id: int) -> bool | None:
    """
    The is_pet_in_db function checks if a pet with the given id exists in the database.

    :param session: AsyncSession: SQLAlchemy AsyncSession object
    :param id: int: Еhe id of the pet that we want to check
    :return: A boolean or none
    """
    query = select(exists(Pet).where(Pet.id == id))
    pet = await session.execute(query)
    return pet.scalar()


async def update_pet_by_id(session: AsyncSession, id: int, **kwargs):
    """
    The update_pet_by_id function updates a pet in database by id.

    :param session: AsyncSession: SQLAlchemy AsyncSession object
    :param id: int: Id of the pet to be updated
    :param **kwargs: The values that will be updated
    :return: The updated pet object
    """
    query = update(Pet).where(Pet.id == id).values(kwargs).returning(Pet)
    result = await session.execute(query)
    updated_pet = result.scalar()
    await session.commit()
    await session.refresh(updated_pet)
    return updated_pet
