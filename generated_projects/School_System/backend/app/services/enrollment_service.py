"""
Enrollment Service
"""

from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment

from app.repositories.enrollment_repository import (
    EnrollmentRepository,
)


class EnrollmentService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Enrollment(
            **data.model_dump()
        )

        return EnrollmentRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return EnrollmentRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return EnrollmentRepository.get_all(
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

        return EnrollmentRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return EnrollmentRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return EnrollmentRepository.exists(
            db,
            obj_id,
        )
