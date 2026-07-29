"""
Patient Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class PatientBase(BaseModel):
    name: str
    age: int
    address: str
    phone: str
    email: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None


class PatientResponse(PatientBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
