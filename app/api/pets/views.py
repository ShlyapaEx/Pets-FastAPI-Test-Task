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
    pets_query = await get_pets(session, limit)
    items = pets_query.all()
    return {'count': len(items), 'items': items}


@pets_router.post('/', response_model=PetReadSchema)
async def create_pet(*, session: AsyncSession = Depends(get_db_session),
                     pet: PetCreateSchema):
    new_pet = await create_new_pet(session, pet)
    return new_pet


@pets_router.delete('/', response_model=PetDeleteResponseSchema)
async def delete_pets(*, session: AsyncSession = Depends(get_db_session),
                      ids: Annotated[conlist(item_type=PositiveInt,
                                             unique_items=True, min_items=1),
                                     Body(example=[1, 2, 3])]):
    errors = []
    existing_pets = await get_existing_pets_ids(session, ids)
    existing_pets_ids = existing_pets.all()

    not_existing_ids = set(ids) - set(existing_pets_ids)
    for bad_id in not_existing_ids:
        errors.append({'id': bad_id,
                       'error': 'Pet with the matching ID was not found.'})

    await delete_many_pets(session, existing_pets_ids)
    return {'deleted': len(existing_pets_ids), 'errors': errors}
