"""
Loan Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class LoanBase(BaseModel):
    loan_type: str
    amount: str
    interest_rate: str
    tenure_months: int
    status: str


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    loan_type: str | None = None
    amount: str | None = None
    interest_rate: str | None = None
    tenure_months: int | None = None
    status: str | None = None


class LoanResponse(LoanBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
