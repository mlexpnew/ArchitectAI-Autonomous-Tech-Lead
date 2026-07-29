"""
Staff Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class StaffBase(BaseModel):
    name: str
    designation: str


class StaffCreate(StaffBase):
    pass


class StaffUpdate(BaseModel):
    name: str | None = None
    designation: str | None = None


class StaffResponse(StaffBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
