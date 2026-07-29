"""
Course Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class CourseBase(BaseModel):
    title: str
    credits: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: str | None = None
    credits: int | None = None


class CourseResponse(CourseBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
