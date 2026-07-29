"""
Invoice Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class InvoiceBase(BaseModel):
    patient_id: int
    appointment_id: int
    medicine_id: int
    total: float
    paid: bool


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    patient_id: int | None = None
    appointment_id: int | None = None
    medicine_id: int | None = None
    total: float | None = None
    paid: bool | None = None


class InvoiceResponse(InvoiceBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
