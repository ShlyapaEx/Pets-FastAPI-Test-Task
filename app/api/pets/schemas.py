from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt

from api.pets.models import PetTypes

LETTER_MATCH_PATTERN = '^[а-яА-Яa-zA-Z\-]+$'


class PetBaseSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100, regex=LETTER_MATCH_PATTERN)
    age: NonNegativeInt
    type: PetTypes


class PetCreateSchema(PetBaseSchema):
    class Config:
        orm_mode = True


class PetUpdateSchema(PetBaseSchema):
    id: PositiveInt
    name: str | None = Field(min_length=1, max_length=100,
                             regex=LETTER_MATCH_PATTERN)
    age: NonNegativeInt | None
    type: PetTypes | None

    class Config:
        orm_mode = True


class PetReadSchema(PetBaseSchema):
    id: PositiveInt
    created_at: datetime

    class Config:
        orm_mode = True


class PetReadListWithCountSchema(BaseModel):
    count: int
    items: list[PetReadSchema] = []


class PetNotExistingErrorSchema(BaseModel):
    id: PositiveInt
    error: str = 'Pet with the matching ID was not found.'


class PetDeleteResponseSchema(BaseModel):
    deleted: int
    errors: list[PetNotExistingErrorSchema]
