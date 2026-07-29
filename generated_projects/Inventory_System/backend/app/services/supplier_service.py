"""
Supplier Service
"""

from sqlalchemy.orm import Session

from app.models.supplier import Supplier

from app.repositories.supplier_repository import (
    SupplierRepository,
)


class SupplierService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Supplier(
            **data.model_dump()
        )

        return SupplierRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return SupplierRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return SupplierRepository.get_all(
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

        return SupplierRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return SupplierRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return SupplierRepository.exists(
            db,
            obj_id,
        )
