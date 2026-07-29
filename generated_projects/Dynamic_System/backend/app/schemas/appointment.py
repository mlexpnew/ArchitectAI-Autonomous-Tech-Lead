"""
Appointment Schemas
"""

from datetime import date as DateType, time as TimeType

from pydantic import BaseModel
from pydantic import ConfigDict


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: DateType
    time: TimeType


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: int | None = None
    doctor_id: int | None = None
    date: DateType | None = None
    time: TimeType | None = None


class AppointmentResponse(AppointmentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
