"""
Appointment Service
"""

from sqlalchemy.orm import Session

from app.repositories.appointment_repository import AppointmentRepository


class AppointmentService:

    @staticmethod
    def get_all(db: Session):

        return AppointmentRepository.get_all(db)
