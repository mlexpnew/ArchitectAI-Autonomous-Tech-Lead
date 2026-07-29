"""
Book Model
"""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time

from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):

    __tablename__ = "books"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String,
    )

    isbn = Column(
        String,
    )

    publication_year = Column(
        Integer,
    )

    available_copies = Column(
        Integer,
    )
