"""
Appointment Schema
"""

from pydantic import BaseModel


class AppointmentCreate(BaseModel):

    patient_id: int

    doctor_id: int

    appointment_date: str

    status: str


class AppointmentResponse(AppointmentCreate):

    id: int

    class Config:

        from_attributes = True
