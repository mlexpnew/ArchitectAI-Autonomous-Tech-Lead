"""
Course Service
"""

from sqlalchemy.orm import Session

from app.models.course import Course

from app.repositories.course_repository import (
    CourseRepository,
)


class CourseService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Course(
            **data.model_dump()
        )

        return CourseRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return CourseRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return CourseRepository.get_all(
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

        return CourseRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return CourseRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return CourseRepository.exists(
            db,
            obj_id,
        )
