"""
Inventory Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class InventoryBase(BaseModel):
    quantity: int
    last_updated: str


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    quantity: int | None = None
    last_updated: str | None = None


class InventoryResponse(InventoryBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
