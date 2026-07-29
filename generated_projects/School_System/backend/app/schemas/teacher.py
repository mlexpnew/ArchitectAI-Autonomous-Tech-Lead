"""
Teacher Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class TeacherBase(BaseModel):
    name: str
    email: str
    designation: str


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    designation: str | None = None


class TeacherResponse(TeacherBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
