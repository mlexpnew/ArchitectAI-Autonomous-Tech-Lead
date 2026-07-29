"""
Cart Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class CartBase(BaseModel):
    created_at: str


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    created_at: str | None = None


class CartResponse(CartBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
