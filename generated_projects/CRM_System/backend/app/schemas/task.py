"""
Task Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class TaskBase(BaseModel):
    title: str
    due_date: DateType
    status: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    due_date: DateType | None = None
    status: str | None = None


class TaskResponse(TaskBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
