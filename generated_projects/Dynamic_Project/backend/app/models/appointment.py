"""
Appointment Model
"""

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    patient_id = Column(Integer)

    doctor_id = Column(Integer)

    appointment_date = Column(String)

    status = Column(String)
