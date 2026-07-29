"""
Patient Schema
"""

from pydantic import BaseModel


class PatientCreate(BaseModel):

    name: str

    age: int

    gender: str

    phone: str


class PatientUpdate(BaseModel):

    name: str | None = None

    age: int | None = None

    gender: str | None = None

    phone: str | None = None


class PatientResponse(PatientCreate):

    id: int

    class Config:

        from_attributes = True
