"""
OrderItem Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class OrderItemBase(BaseModel):
    quantity: int
    unit_price: str


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: int | None = None
    unit_price: str | None = None


class OrderItemResponse(OrderItemBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
