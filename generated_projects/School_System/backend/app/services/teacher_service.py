"""
Teacher Service
"""

from sqlalchemy.orm import Session

from app.models.teacher import Teacher

from app.repositories.teacher_repository import (
    TeacherRepository,
)


class TeacherService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Teacher(
            **data.model_dump()
        )

        return TeacherRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return TeacherRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return TeacherRepository.get_all(
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

        return TeacherRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return TeacherRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return TeacherRepository.exists(
            db,
            obj_id,
        )
