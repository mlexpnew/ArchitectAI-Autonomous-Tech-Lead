"""
Doctor Service
"""

from sqlalchemy.orm import Session

from app.repositories.doctor_repository import DoctorRepository


class DoctorService:

    @staticmethod
    def get_all(db: Session):

        return DoctorRepository.get_all(db)
