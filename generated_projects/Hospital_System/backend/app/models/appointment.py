"""
Appointment Model
"""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time

from sqlalchemy.orm import relationship

from app.database import Base


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
    )

    appointment_date = Column(
        Date,
    )

    patient = relationship(
        "Patient",
        foreign_keys=[patient_id],
    )

    doctor = relationship(
        "Doctor",
        foreign_keys=[doctor_id],
    )
