from typing import Annotated

from fastapi import APIRouter, Depends, Body
from pydantic import conlist
from sqlalchemy.ext.asyncio import AsyncSession

from api.pets.queries import create_new_pet, get_pets, is_pet_existing, delete_many_pets
from api.pets.schemas import (PetCreateSchema, PetReadListWithCountSchema,
                              PetReadSchema)
from db.database import get_db_session

pets_router = APIRouter()


@pets_router.get('/', response_model=PetReadListWithCountSchema)
async def list_pets(session: AsyncSession = Depends(get_db_session),
                    limit: int | None = 20):
    pets_query = await get_pets(session, limit)
    items = pets_query.all()
    return {'count': len(items), 'items': items}


@pets_router.post('/', response_model=PetReadSchema)
async def create_pet(*, session: AsyncSession = Depends(get_db_session),
                     pet: PetCreateSchema):
    new_pet = await create_new_pet(session, pet)
    return new_pet


@pets_router.delete('/')
async def delete_pets(*, session: AsyncSession = Depends(get_db_session),
                      ids: Annotated[conlist(item_type=int, unique_items=True,
                                             min_items=1), Body()]):  # type: ignore
    errors = []
    for pet_id in ids[:]:
        if not await is_pet_existing(session, pet_id):
            errors.append({'id': pet_id,
                           'error': 'Pet with the matching ID was not found.'})
            ids.remove(pet_id)
    await delete_many_pets(session, ids)
    return {'deleted': len(ids), 'errors': errors}
