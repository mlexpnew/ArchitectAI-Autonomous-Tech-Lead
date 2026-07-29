"""
Department Service
"""

from sqlalchemy.orm import Session

from app.models.department import Department

from app.repositories.department_repository import (
    DepartmentRepository,
)


class DepartmentService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Department(
            **data.model_dump()
        )

        return DepartmentRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return DepartmentRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return DepartmentRepository.get_all(
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

        return DepartmentRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return DepartmentRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return DepartmentRepository.exists(
            db,
            obj_id,
        )
