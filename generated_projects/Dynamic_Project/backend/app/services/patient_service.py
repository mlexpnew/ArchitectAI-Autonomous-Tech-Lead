"""
Patient Service
"""

from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.repositories.patient_repository import PatientRepository


class PatientService:

    @staticmethod
    def get_all(db: Session):

        return PatientRepository.get_all(db)


    @staticmethod
    def get_by_id(
        db: Session,
        patient_id: int,
    ):

        return PatientRepository.get_by_id(
            db,
            patient_id,
        )


    @staticmethod
    def create(
        db: Session,
        data,
    ):

        patient = Patient(**data.model_dump())

        return PatientRepository.create(
            db,
            patient,
        )


    @staticmethod
    def delete(
        db: Session,
        patient_id: int,
    ):

        return PatientRepository.delete(
            db,
            patient_id,
        )
