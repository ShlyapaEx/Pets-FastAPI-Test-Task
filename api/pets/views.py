from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.pets.queries import create_new_pet, get_pets
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
