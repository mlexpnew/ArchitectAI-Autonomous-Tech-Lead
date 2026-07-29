"""
Hospital Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class HospitalBase(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str


class HospitalCreate(HospitalBase):
    pass


class HospitalUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone_number: str | None = None
    email: str | None = None


class HospitalResponse(HospitalBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
