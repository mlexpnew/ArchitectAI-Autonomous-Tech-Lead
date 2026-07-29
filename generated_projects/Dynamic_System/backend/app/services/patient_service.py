"""
Patient Service
"""

from sqlalchemy.orm import Session

from app.models.patient import Patient

from app.repositories.patient_repository import (
    PatientRepository,
)


class PatientService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Patient(
            **data.model_dump()
        )

        return PatientRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return PatientRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return PatientRepository.get_all(
            db,
            skip=skip,
            limit=limit,
        )


    @staticmethod
    def update(
        db: Session,
        obj_id: int,
        data,
    ):
        update_data = data.model_dump(
            exclude_unset=True
        )

        return PatientRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return PatientRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return PatientRepository.exists(
            db,
            obj_id,
        )
