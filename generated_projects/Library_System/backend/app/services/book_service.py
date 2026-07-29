"""
Book Service
"""

from sqlalchemy.orm import Session

from app.models.book import Book

from app.repositories.book_repository import (
    BookRepository,
)


class BookService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Book(
            **data.model_dump()
        )

        return BookRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return BookRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return BookRepository.get_all(
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

        return BookRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return BookRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return BookRepository.exists(
            db,
            obj_id,
        )
