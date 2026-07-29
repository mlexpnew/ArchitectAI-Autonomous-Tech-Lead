"""
Doctor Service
"""

from sqlalchemy.orm import Session

from app.models.doctor import Doctor

from app.repositories.doctor_repository import (
    DoctorRepository,
)


class DoctorService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Doctor(
            **data.model_dump()
        )

        return DoctorRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return DoctorRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return DoctorRepository.get_all(
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

        return DoctorRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return DoctorRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return DoctorRepository.exists(
            db,
            obj_id,
        )
