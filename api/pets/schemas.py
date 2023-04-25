import re
from datetime import datetime

from pydantic import BaseModel, Field

from api.pets.models import PetTypes

LETTER_MATCH_PATTERN = '^[а-яА-Яa-zA-Z\-]+$'


class PetBaseSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100, regex=LETTER_MATCH_PATTERN)
    age: int = Field(gt=0)
    type: PetTypes


class PetCreateSchema(PetBaseSchema):
    class Config:
        orm_mode = True


class PetReadSchema(PetBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PetReadListWithCountSchema(BaseModel):
    count: int
    items: list[PetReadSchema] = []
