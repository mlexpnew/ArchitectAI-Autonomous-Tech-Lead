"""
Opportunity Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class OpportunityBase(BaseModel):
    title: str
    value: str
    stage: str


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    title: str | None = None
    value: str | None = None
    stage: str | None = None


class OpportunityResponse(OpportunityBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
