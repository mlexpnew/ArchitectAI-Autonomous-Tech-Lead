"""
Doctor Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class DoctorBase(BaseModel):
    name: str
    specialization: str


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: str | None = None
    specialization: str | None = None


class DoctorResponse(DoctorBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
