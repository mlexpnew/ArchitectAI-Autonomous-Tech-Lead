"""
Customer Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str
    created_at: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    password: str | None = None
    created_at: str | None = None


class CustomerResponse(CustomerBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
