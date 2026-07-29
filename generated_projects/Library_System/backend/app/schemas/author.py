"""
Author Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class AuthorBase(BaseModel):
    first_name: str
    last_name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class AuthorResponse(AuthorBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
