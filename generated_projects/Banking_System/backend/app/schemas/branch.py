"""
Branch Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class BranchBase(BaseModel):
    branch_name: str
    branch_code: str
    city: str


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    branch_name: str | None = None
    branch_code: str | None = None
    city: str | None = None


class BranchResponse(BranchBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
