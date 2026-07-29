"""
Reservation Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class ReservationBase(BaseModel):
    check_in: DateType
    check_out: DateType
    status: str


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    check_in: DateType | None = None
    check_out: DateType | None = None
    status: str | None = None


class ReservationResponse(ReservationBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
