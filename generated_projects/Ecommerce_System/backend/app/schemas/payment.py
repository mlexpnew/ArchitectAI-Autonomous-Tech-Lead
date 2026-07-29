"""
Payment Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class PaymentBase(BaseModel):
    payment_method: str
    payment_status: str
    payment_date: str
    amount: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    payment_method: str | None = None
    payment_status: str | None = None
    payment_date: str | None = None
    amount: str | None = None


class PaymentResponse(PaymentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
