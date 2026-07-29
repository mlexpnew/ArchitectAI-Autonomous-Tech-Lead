"""
Account Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class AccountBase(BaseModel):
    account_number: str
    account_type: str
    balance: str
    status: str
    created_at: str


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    account_number: str | None = None
    account_type: str | None = None
    balance: str | None = None
    status: str | None = None
    created_at: str | None = None


class AccountResponse(AccountBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
