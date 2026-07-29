"""
BorrowRecord Service
"""

from sqlalchemy.orm import Session

from app.models.borrowrecord import BorrowRecord

from app.repositories.borrowrecord_repository import (
    BorrowRecordRepository,
)


class BorrowRecordService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = BorrowRecord(
            **data.model_dump()
        )

        return BorrowRecordRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return BorrowRecordRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return BorrowRecordRepository.get_all(
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

        return BorrowRecordRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return BorrowRecordRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return BorrowRecordRepository.exists(
            db,
            obj_id,
        )
