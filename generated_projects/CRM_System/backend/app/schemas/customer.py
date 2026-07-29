"""
Customer Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class CustomerResponse(CustomerBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
