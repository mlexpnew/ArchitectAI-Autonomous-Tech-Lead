"""
Inventory Service
"""

from sqlalchemy.orm import Session

from app.models.inventory import Inventory

from app.repositories.inventory_repository import (
    InventoryRepository,
)


class InventoryService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Inventory(
            **data.model_dump()
        )

        return InventoryRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return InventoryRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return InventoryRepository.get_all(
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

        return InventoryRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return InventoryRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return InventoryRepository.exists(
            db,
            obj_id,
        )
