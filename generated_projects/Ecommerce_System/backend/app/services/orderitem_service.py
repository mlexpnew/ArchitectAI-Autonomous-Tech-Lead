"""
OrderItem Service
"""

from sqlalchemy.orm import Session

from app.models.orderitem import OrderItem

from app.repositories.orderitem_repository import (
    OrderItemRepository,
)


class OrderItemService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = OrderItem(
            **data.model_dump()
        )

        return OrderItemRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return OrderItemRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return OrderItemRepository.get_all(
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

        return OrderItemRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return OrderItemRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return OrderItemRepository.exists(
            db,
            obj_id,
        )
