"""
Warehouse Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class WarehouseBase(BaseModel):
    name: str
    city: str


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    name: str | None = None
    city: str | None = None


class WarehouseResponse(WarehouseBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
