"""
Task Service
"""

from sqlalchemy.orm import Session

from app.models.task import Task

from app.repositories.task_repository import (
    TaskRepository,
)


class TaskService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Task(
            **data.model_dump()
        )

        return TaskRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return TaskRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return TaskRepository.get_all(
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

        return TaskRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return TaskRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return TaskRepository.exists(
            db,
            obj_id,
        )
