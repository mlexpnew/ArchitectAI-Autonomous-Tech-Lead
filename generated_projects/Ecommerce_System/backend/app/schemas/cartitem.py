"""
CartItem Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class CartItemBase(BaseModel):
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int | None = None


class CartItemResponse(CartItemBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
