"""
Card Service
"""

from sqlalchemy.orm import Session

from app.models.card import Card

from app.repositories.card_repository import (
    CardRepository,
)


class CardService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Card(
            **data.model_dump()
        )

        return CardRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return CardRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return CardRepository.get_all(
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

        return CardRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return CardRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return CardRepository.exists(
            db,
            obj_id,
        )
