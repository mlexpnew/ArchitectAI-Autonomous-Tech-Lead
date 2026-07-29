"""
Supplier Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class SupplierBase(BaseModel):
    name: str
    email: str


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


class SupplierResponse(SupplierBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
