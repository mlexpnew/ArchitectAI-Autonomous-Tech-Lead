"""
Employee Service
"""

from sqlalchemy.orm import Session

from app.models.employee import Employee

from app.repositories.employee_repository import (
    EmployeeRepository,
)


class EmployeeService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Employee(
            **data.model_dump()
        )

        return EmployeeRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return EmployeeRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return EmployeeRepository.get_all(
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

        return EmployeeRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return EmployeeRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return EmployeeRepository.exists(
            db,
            obj_id,
        )
