"""
Opportunity Service
"""

from sqlalchemy.orm import Session

from app.models.opportunity import Opportunity

from app.repositories.opportunity_repository import (
    OpportunityRepository,
)


class OpportunityService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Opportunity(
            **data.model_dump()
        )

        return OpportunityRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return OpportunityRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return OpportunityRepository.get_all(
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

        return OpportunityRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return OpportunityRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return OpportunityRepository.exists(
            db,
            obj_id,
        )
