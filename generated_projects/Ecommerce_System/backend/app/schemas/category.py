"""
Category Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryResponse(CategoryBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
