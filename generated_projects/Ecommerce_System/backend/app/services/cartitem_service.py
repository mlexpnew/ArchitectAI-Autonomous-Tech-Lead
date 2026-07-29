"""
CartItem Service
"""

from sqlalchemy.orm import Session

from app.models.cartitem import CartItem

from app.repositories.cartitem_repository import (
    CartItemRepository,
)


class CartItemService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = CartItem(
            **data.model_dump()
        )

        return CartItemRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return CartItemRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return CartItemRepository.get_all(
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

        return CartItemRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return CartItemRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return CartItemRepository.exists(
            db,
            obj_id,
        )
