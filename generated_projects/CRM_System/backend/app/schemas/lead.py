"""
Lead Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class LeadBase(BaseModel):
    name: str
    email: str
    status: str


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    status: str | None = None


class LeadResponse(LeadBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
