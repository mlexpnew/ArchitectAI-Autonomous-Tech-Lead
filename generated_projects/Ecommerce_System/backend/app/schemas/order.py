"""
Order Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class OrderBase(BaseModel):
    order_date: str
    total_amount: str
    order_status: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_date: str | None = None
    total_amount: str | None = None
    order_status: str | None = None


class OrderResponse(OrderBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
