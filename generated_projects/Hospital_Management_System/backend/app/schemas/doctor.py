"""
Doctor Schema
"""

from pydantic import BaseModel


class DoctorCreate(BaseModel):

    name: str

    specialization: str

    experience: int


class DoctorResponse(DoctorCreate):

    id: int

    class Config:

        from_attributes = True
