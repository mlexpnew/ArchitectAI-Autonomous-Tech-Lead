"""
Hospital Service
"""

from sqlalchemy.orm import Session

from app.models.hospital import Hospital

from app.repositories.hospital_repository import (
    HospitalRepository,
)


class HospitalService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Hospital(
            **data.model_dump()
        )

        return HospitalRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return HospitalRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return HospitalRepository.get_all(
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

        return HospitalRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return HospitalRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return HospitalRepository.exists(
            db,
            obj_id,
        )
