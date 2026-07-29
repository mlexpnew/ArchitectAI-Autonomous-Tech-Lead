"""
Appointment Service
"""

from sqlalchemy.orm import Session

from app.models.appointment import Appointment

from app.repositories.appointment_repository import (
    AppointmentRepository,
)


class AppointmentService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Appointment(
            **data.model_dump()
        )

        return AppointmentRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return AppointmentRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return AppointmentRepository.get_all(
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

        return AppointmentRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return AppointmentRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return AppointmentRepository.exists(
            db,
            obj_id,
        )
