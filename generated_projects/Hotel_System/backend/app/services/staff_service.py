"""
Staff Service
"""

from sqlalchemy.orm import Session

from app.models.staff import Staff

from app.repositories.staff_repository import (
    StaffRepository,
)


class StaffService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Staff(
            **data.model_dump()
        )

        return StaffRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return StaffRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return StaffRepository.get_all(
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

        return StaffRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return StaffRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return StaffRepository.exists(
            db,
            obj_id,
        )
