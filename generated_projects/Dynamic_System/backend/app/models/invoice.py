"""
Invoice Model
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


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
    )

    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id"),
    )

    medicine_id = Column(
        Integer,
        ForeignKey("medicines.id"),
    )

    total = Column(
        Float,
    )

    paid = Column(
        Boolean,
    )

    patient = relationship(
        "Patient",
        foreign_keys=[patient_id],
    )

    appointment = relationship(
        "Appointment",
        foreign_keys=[appointment_id],
    )

    medicine = relationship(
        "Medicine",
        foreign_keys=[medicine_id],
    )
