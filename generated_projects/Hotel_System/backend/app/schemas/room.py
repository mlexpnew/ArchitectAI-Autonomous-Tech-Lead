"""
Room Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class RoomBase(BaseModel):
    room_number: str
    room_type: str
    price: str
    status: str


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    room_number: str | None = None
    room_type: str | None = None
    price: str | None = None
    status: str | None = None


class RoomResponse(RoomBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
