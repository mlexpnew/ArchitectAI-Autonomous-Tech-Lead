"""
Patient Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class PatientBase(BaseModel):
    name: str
    age: int
    gender: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: str | None = None


class PatientResponse(PatientBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
