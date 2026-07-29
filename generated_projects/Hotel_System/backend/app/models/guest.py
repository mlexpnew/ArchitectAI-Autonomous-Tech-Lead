"""
Guest Model
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


class Guest(Base):

    __tablename__ = "guests"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
    )

    phone = Column(
        String,
    )

    email = Column(
        String,
    )
