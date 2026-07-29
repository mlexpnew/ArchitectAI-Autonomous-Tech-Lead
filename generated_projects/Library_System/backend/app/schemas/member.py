"""
Member Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class MemberBase(BaseModel):
    name: str
    email: str
    phone: str
    membership_date: DateType


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    membership_date: DateType | None = None


class MemberResponse(MemberBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
