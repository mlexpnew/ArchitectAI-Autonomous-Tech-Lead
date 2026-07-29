"""
Category Service
"""

from sqlalchemy.orm import Session

from app.models.category import Category

from app.repositories.category_repository import (
    CategoryRepository,
)


class CategoryService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Category(
            **data.model_dump()
        )

        return CategoryRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return CategoryRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return CategoryRepository.get_all(
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

        return CategoryRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return CategoryRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return CategoryRepository.exists(
            db,
            obj_id,
        )
