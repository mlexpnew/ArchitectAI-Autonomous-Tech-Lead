"""
PurchaseOrder Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class PurchaseOrderBase(BaseModel):
    order_date: DateType
    status: str


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderUpdate(BaseModel):
    order_date: DateType | None = None
    status: str | None = None


class PurchaseOrderResponse(PurchaseOrderBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
