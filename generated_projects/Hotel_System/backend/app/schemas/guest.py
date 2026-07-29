"""
Guest Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class GuestBase(BaseModel):
    name: str
    phone: str
    email: str


class GuestCreate(GuestBase):
    pass


class GuestUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None


class GuestResponse(GuestBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
