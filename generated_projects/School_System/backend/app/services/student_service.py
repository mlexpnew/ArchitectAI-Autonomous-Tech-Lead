"""
Student Service
"""

from sqlalchemy.orm import Session

from app.models.student import Student

from app.repositories.student_repository import (
    StudentRepository,
)


class StudentService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Student(
            **data.model_dump()
        )

        return StudentRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return StudentRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return StudentRepository.get_all(
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

        return StudentRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return StudentRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return StudentRepository.exists(
            db,
            obj_id,
        )
