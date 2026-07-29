"""
Invoice Service
"""

from sqlalchemy.orm import Session

from app.models.invoice import Invoice

from app.repositories.invoice_repository import (
    InvoiceRepository,
)


class InvoiceService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Invoice(
            **data.model_dump()
        )

        return InvoiceRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return InvoiceRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return InvoiceRepository.get_all(
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

        return InvoiceRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return InvoiceRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return InvoiceRepository.exists(
            db,
            obj_id,
        )
