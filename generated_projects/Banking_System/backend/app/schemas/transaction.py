"""
Transaction Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class TransactionBase(BaseModel):
    transaction_type: str
    amount: str
    transaction_date: str
    description: str


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    transaction_type: str | None = None
    amount: str | None = None
    transaction_date: str | None = None
    description: str | None = None


class TransactionResponse(TransactionBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
