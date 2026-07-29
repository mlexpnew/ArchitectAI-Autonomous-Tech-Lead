"""
Order Service
"""

from sqlalchemy.orm import Session

from app.models.order import Order

from app.repositories.order_repository import (
    OrderRepository,
)


class OrderService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Order(
            **data.model_dump()
        )

        return OrderRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return OrderRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return OrderRepository.get_all(
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

        return OrderRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return OrderRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return OrderRepository.exists(
            db,
            obj_id,
        )
