"""
Author Service
"""

from sqlalchemy.orm import Session

from app.models.author import Author

from app.repositories.author_repository import (
    AuthorRepository,
)


class AuthorService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Author(
            **data.model_dump()
        )

        return AuthorRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return AuthorRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return AuthorRepository.get_all(
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

        return AuthorRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return AuthorRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return AuthorRepository.exists(
            db,
            obj_id,
        )
