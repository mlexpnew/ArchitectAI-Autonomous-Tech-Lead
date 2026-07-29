"""
Student Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class StudentBase(BaseModel):
    name: str
    email: str
    dob: DateType


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    dob: DateType | None = None


class StudentResponse(StudentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
