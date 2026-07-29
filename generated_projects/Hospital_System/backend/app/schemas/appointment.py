"""
Appointment Schemas
"""

from datetime import date as DateType

from pydantic import BaseModel
from pydantic import ConfigDict


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: DateType


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: int | None = None
    doctor_id: int | None = None
    appointment_date: DateType | None = None


class AppointmentResponse(AppointmentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
