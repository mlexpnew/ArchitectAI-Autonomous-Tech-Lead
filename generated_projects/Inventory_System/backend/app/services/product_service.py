"""
Product Service
"""

from sqlalchemy.orm import Session

from app.models.product import Product

from app.repositories.product_repository import (
    ProductRepository,
)


class ProductService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Product(
            **data.model_dump()
        )

        return ProductRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return ProductRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return ProductRepository.get_all(
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

        return ProductRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return ProductRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return ProductRepository.exists(
            db,
            obj_id,
        )
