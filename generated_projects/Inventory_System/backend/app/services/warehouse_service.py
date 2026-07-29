"""
Warehouse Service
"""

from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse

from app.repositories.warehouse_repository import (
    WarehouseRepository,
)


class WarehouseService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Warehouse(
            **data.model_dump()
        )

        return WarehouseRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return WarehouseRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return WarehouseRepository.get_all(
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

        return WarehouseRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return WarehouseRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return WarehouseRepository.exists(
            db,
            obj_id,
        )
