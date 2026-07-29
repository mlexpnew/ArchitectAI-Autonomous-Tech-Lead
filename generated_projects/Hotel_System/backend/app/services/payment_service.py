"""
Payment Service
"""

from sqlalchemy.orm import Session

from app.models.payment import Payment

from app.repositories.payment_repository import (
    PaymentRepository,
)


class PaymentService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Payment(
            **data.model_dump()
        )

        return PaymentRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return PaymentRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return PaymentRepository.get_all(
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

        return PaymentRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return PaymentRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return PaymentRepository.exists(
            db,
            obj_id,
        )
