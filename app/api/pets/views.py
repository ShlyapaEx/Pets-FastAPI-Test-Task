from typing import Annotated

from fastapi import APIRouter, Body, Depends
from pydantic import PositiveInt, conlist
from sqlalchemy.ext.asyncio import AsyncSession

from api.pets.queries import (create_new_pet, delete_many_pets,
                              get_existing_pets_ids, get_pets)
from api.pets.schemas import (PetCreateSchema, PetDeleteResponseSchema,
                              PetReadListWithCountSchema, PetReadSchema)
from db.database import get_db_session

pets_router = APIRouter()


@pets_router.get('/', response_model=PetReadListWithCountSchema)
async def list_pets(session: AsyncSession = Depends(get_db_session),
                    limit: int | None = 20):
    """
    The list_pets route returns a list of pets from database.

    :param session: AsyncSession: Get the database session
    :param limit: int | None: Limit the number of pets returned
    :return: A dict with two keys: count and items
    """
    pets_query = await get_pets(session, limit)
    items = pets_query.all()
    return {'count': len(items), 'items': items}


@pets_router.post('/', response_model=PetReadSchema)
async def create_pet(*, session: AsyncSession = Depends(get_db_session),
                     pet: PetCreateSchema):
    """
    The create_pet route creates a new pet in the database.

    :param session: AsyncSession: Get the database session
    :param pet: PetCreateSchema: Validate the data that is passed to the function
    :return: A newly created pet object
    """
    new_pet = await create_new_pet(session, pet)
    return new_pet


@pets_router.delete('/', response_model=PetDeleteResponseSchema)
async def delete_pets(*, session: AsyncSession = Depends(get_db_session),
                      ids: Annotated[conlist(item_type=PositiveInt,
                                             unique_items=True, min_items=1),
                                     Body(example=[1, 2, 3])]):
    """
    The delete_pets route deletes pets by their IDs.
    Before deleting it checks that pets actually exist in database
    and deletes them if so. Otherwise it adds non-existing pet ids to error list.

    :param session: AsyncSession: Get the database session
    :param ids: list of pet ids to delete from database
    :return: A dictionary with two keys: count of deleted pets and list of errors
    """
    errors = []
    existing_pets = await get_existing_pets_ids(session, ids)
    existing_pets_ids = existing_pets.all()

    not_existing_ids = set(ids) - set(existing_pets_ids)
    for bad_id in not_existing_ids:
        errors.append({'id': bad_id,
                       'error': 'Pet with the matching ID was not found.'})

    await delete_many_pets(session, existing_pets_ids)
    return {'deleted': len(existing_pets_ids), 'errors': errors}
