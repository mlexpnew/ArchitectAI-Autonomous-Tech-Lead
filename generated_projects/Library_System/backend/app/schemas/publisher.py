"""
Publisher Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class PublisherBase(BaseModel):
    name: str
    city: str


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(BaseModel):
    name: str | None = None
    city: str | None = None


class PublisherResponse(PublisherBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
