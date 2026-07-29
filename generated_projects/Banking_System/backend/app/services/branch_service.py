"""
Branch Service
"""

from sqlalchemy.orm import Session

from app.models.branch import Branch

from app.repositories.branch_repository import (
    BranchRepository,
)


class BranchService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Branch(
            **data.model_dump()
        )

        return BranchRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return BranchRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return BranchRepository.get_all(
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

        return BranchRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return BranchRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return BranchRepository.exists(
            db,
            obj_id,
        )
