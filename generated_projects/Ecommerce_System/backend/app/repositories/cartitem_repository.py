"""
CartItem Repository
"""

from sqlalchemy.orm import Session

from app.models.cartitem import CartItem


class CartItemRepository:

    @staticmethod
    def create(
        db: Session,
        obj: CartItem,
    ):
        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return (
            db.query(CartItem)
            .filter(CartItem.id == obj_id)
            .first()
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return (
            db.query(CartItem)
            .offset(skip)
            .limit(limit)
            .all()
        )


    @staticmethod
    def update(
        db: Session,
        obj_id: int,
        data: dict,
    ):
        obj = (
            db.query(CartItem)
            .filter(CartItem.id == obj_id)
            .first()
        )

        if obj is None:
            return None

        for key, value in data.items():

            if key == "id":
                continue

            if hasattr(obj, key):
                setattr(obj, key, value)

        db.commit()
        db.refresh(obj)

        return obj


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        obj = (
            db.query(CartItem)
            .filter(CartItem.id == obj_id)
            .first()
        )

        if obj is None:
            return None

        db.delete(obj)
        db.commit()

        return obj


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return (
            db.query(CartItem.id)
            .filter(CartItem.id == obj_id)
            .first()
            is not None
        )
