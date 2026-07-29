"""
Customer Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: DateType
    created_at: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    date_of_birth: DateType | None = None
    created_at: str | None = None


class CustomerResponse(CustomerBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
