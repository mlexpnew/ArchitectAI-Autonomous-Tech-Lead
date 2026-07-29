"""
Department Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = None


class DepartmentResponse(DepartmentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
