"""
Room Service
"""

from sqlalchemy.orm import Session

from app.models.room import Room

from app.repositories.room_repository import (
    RoomRepository,
)


class RoomService:

    @staticmethod
    def create(
        db: Session,
        data,
    ):
        obj = Room(
            **data.model_dump()
        )

        return RoomRepository.create(
            db,
            obj,
        )


    @staticmethod
    def get_by_id(
        db: Session,
        obj_id: int,
    ):
        return RoomRepository.get_by_id(
            db,
            obj_id,
        )


    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        return RoomRepository.get_all(
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

        return RoomRepository.update(
            db,
            obj_id,
            update_data,
        )


    @staticmethod
    def delete(
        db: Session,
        obj_id: int,
    ):
        return RoomRepository.delete(
            db,
            obj_id,
        )


    @staticmethod
    def exists(
        db: Session,
        obj_id: int,
    ) -> bool:
        return RoomRepository.exists(
            db,
            obj_id,
        )
