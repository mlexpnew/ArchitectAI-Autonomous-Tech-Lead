"""
Employee Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class EmployeeBase(BaseModel):
    name: str
    department: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = None
    department: str | None = None


class EmployeeResponse(EmployeeBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
