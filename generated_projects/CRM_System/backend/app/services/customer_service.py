"""
Customer Service
"""

from sqlalchemy.orm import Session

from app.models.customer import Customer

from app.repositories.customer_repository import (
    CustomerRepository,
)


class CustomerService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Customer(
            **data.model_dump()
        )

        return CustomerRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return CustomerRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return CustomerRepository.get_all(
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

        return CustomerRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return CustomerRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return CustomerRepository.exists(
            db,
            obj_id,
        )
