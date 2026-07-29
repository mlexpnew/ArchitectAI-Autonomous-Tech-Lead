"""
Card Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class CardBase(BaseModel):
    card_number: str
    expiry_date: DateType
    cvv: str
    card_type: str


class CardCreate(CardBase):
    pass


class CardUpdate(BaseModel):
    card_number: str | None = None
    expiry_date: DateType | None = None
    cvv: str | None = None
    card_type: str | None = None


class CardResponse(CardBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
