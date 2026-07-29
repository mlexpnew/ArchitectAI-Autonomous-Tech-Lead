"""
Reservation Service
"""

from sqlalchemy.orm import Session

from app.models.reservation import Reservation

from app.repositories.reservation_repository import (
    ReservationRepository,
)


class ReservationService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Reservation(
            **data.model_dump()
        )

        return ReservationRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return ReservationRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return ReservationRepository.get_all(
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

        return ReservationRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return ReservationRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return ReservationRepository.exists(
            db,
            obj_id,
        )
