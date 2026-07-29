"""
Book Schemas
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: int
    available_copies: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    isbn: str | None = None
    publication_year: int | None = None
    available_copies: int | None = None


class BookResponse(BookBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
