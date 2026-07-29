"""
PurchaseOrder Service
"""

from sqlalchemy.orm import Session

from app.models.purchaseorder import PurchaseOrder

from app.repositories.purchaseorder_repository import (
    PurchaseOrderRepository,
)


class PurchaseOrderService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = PurchaseOrder(
            **data.model_dump()
        )

        return PurchaseOrderRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return PurchaseOrderRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return PurchaseOrderRepository.get_all(
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

        return PurchaseOrderRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return PurchaseOrderRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return PurchaseOrderRepository.exists(
            db,
            obj_id,
        )
