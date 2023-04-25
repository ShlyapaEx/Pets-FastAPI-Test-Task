from datetime import datetime

from pydantic import BaseModel, Field

from api.pets.models import PetTypes


class PetBaseSchema(BaseModel):
    name: str
    age: int
    type: PetTypes


class PetCreateSchema(PetBaseSchema):
    pass


class PetReadSchema(PetBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PetReadWithCountSchema(BaseModel):
    count: int
    items: list[PetReadSchema] = []
