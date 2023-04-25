from fastapi import APIRouter, Depends
from db.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from api.pets.queries import get_pets
from api.pets.schemas import PetReadWithCountSchema

pets_router = APIRouter()


@pets_router.get('/', response_model=PetReadWithCountSchema)
async def list_pets(session: AsyncSession = Depends(get_db_session),
                    limit: int | None = 20):
    pets_query = await get_pets(session, limit)
    items = pets_query.all()
    return {'count': len(items), 'items': items}
