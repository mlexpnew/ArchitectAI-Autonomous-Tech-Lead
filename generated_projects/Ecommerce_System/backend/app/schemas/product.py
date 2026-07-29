"""
Product Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    sku: str
    price: str
    stock_quantity: int
    status: str
    created_at: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    sku: str | None = None
    price: str | None = None
    stock_quantity: int | None = None
    status: str | None = None
    created_at: str | None = None


class ProductResponse(ProductBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
