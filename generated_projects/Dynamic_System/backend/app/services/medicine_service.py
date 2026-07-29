"""
Medicine Service
"""

from sqlalchemy.orm import Session

from app.models.medicine import Medicine

from app.repositories.medicine_repository import (
    MedicineRepository,
)


class MedicineService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Medicine(
            **data.model_dump()
        )

        return MedicineRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return MedicineRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return MedicineRepository.get_all(
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

        return MedicineRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return MedicineRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return MedicineRepository.exists(
            db,
            obj_id,
        )
