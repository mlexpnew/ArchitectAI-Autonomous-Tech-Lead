"""
Payment Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class PaymentBase(BaseModel):
    amount: str
    payment_date: str
    payment_method: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: str | None = None
    payment_date: str | None = None
    payment_method: str | None = None


class PaymentResponse(PaymentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
