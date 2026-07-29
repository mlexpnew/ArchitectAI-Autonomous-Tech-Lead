"""
Product Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class ProductBase(BaseModel):
    name: str
    sku: str
    price: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    price: str | None = None


class ProductResponse(ProductBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
