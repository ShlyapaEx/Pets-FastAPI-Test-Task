from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class PetTypes(Enum):
    dog = 'dog'
    cat = 'cat'


PetTypesColumn = ENUM(PetTypes, name="type",
                      create_constraint=True, metadata=Base.metadata,
                      validate_strings=True)


class Pet(Base):
    __tablename__ = 'Pet'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer())
    type: Mapped[str] = mapped_column(PetTypesColumn)
    created_at: Mapped[datetime] = mapped_column(DateTime(),
                                                 server_default=func.now())
