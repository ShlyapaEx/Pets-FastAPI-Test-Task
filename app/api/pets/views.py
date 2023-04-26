from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import PositiveInt, conlist
from sqlalchemy.ext.asyncio import AsyncSession

from api.pets.queries import (create_new_pet, delete_many_pets,
                              get_existing_pets_ids, get_pets, is_pet_in_db, update_pet_by_id)
from api.pets.schemas import (PetCreateSchema, PetDeleteResponseSchema,
                              PetReadListWithCountSchema, PetReadSchema,
                              PetUpdateSchema)
from db.database import get_db_session

pets_router = APIRouter()


@pets_router.get('/', response_model=PetReadListWithCountSchema)
async def list_pets(session: AsyncSession = Depends(get_db_session),
                    limit: int | None = 20):
    """
    The list_pets route returns a list of pets from database.
    \f
    :param session: AsyncSession: Get SQLAlchemy async database session using dependency
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
    \f
    :param session: AsyncSession: Get SQLAlchemy async database session using dependency
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
    \f
    :param session: AsyncSession: Get SQLAlchemy async database session using dependency
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


@pets_router.patch('/', response_model=PetReadSchema)
async def update_pet(*, session: AsyncSession = Depends(get_db_session),
                     pet: PetUpdateSchema):
    """
    The update_pet route updates a pet in the database.
    \f
    :param session: AsyncSession: Get SQLAlchemy async database session using dependency
    :param pet: PetUpdateSchema: Get the pet object from the request body
    :return: The updated pet object
    """
    if not await is_pet_in_db(session, pet.id):
        raise HTTPException(status_code=404,
                            detail=f'Pet with id {pet.id} was not found')

    updated_pet_params = pet.dict(exclude_none=True, exclude={'id'})
    new_pet = await update_pet_by_id(session=session, id=pet.id,
                                     **updated_pet_params)
    return new_pet
