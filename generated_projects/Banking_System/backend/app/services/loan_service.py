"""
Loan Service
"""

from sqlalchemy.orm import Session

from app.models.loan import Loan

from app.repositories.loan_repository import (
    LoanRepository,
)


class LoanService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Loan(
            **data.model_dump()
        )

        return LoanRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return LoanRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return LoanRepository.get_all(
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

        return LoanRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return LoanRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return LoanRepository.exists(
            db,
            obj_id,
        )
