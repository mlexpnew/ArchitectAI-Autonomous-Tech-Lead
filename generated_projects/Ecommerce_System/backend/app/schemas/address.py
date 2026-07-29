"""
Address Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None


class AddressResponse(AddressBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
