"""
Address Model
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


class Address(Base):

    __tablename__ = "addresss"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    street = Column(
        String,
    )

    city = Column(
        String,
    )

    state = Column(
        String,
    )

    postal_code = Column(
        String,
    )

    country = Column(
        String,
    )
