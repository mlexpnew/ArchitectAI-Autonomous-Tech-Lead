"""
Lead Service
"""

from sqlalchemy.orm import Session

from app.models.lead import Lead

from app.repositories.lead_repository import (
    LeadRepository,
)


class LeadService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Lead(
            **data.model_dump()
        )

        return LeadRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return LeadRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return LeadRepository.get_all(
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

        return LeadRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return LeadRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return LeadRepository.exists(
            db,
            obj_id,
        )
