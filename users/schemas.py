from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MinLen, MaxLen

from typing import List, Optional


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []
