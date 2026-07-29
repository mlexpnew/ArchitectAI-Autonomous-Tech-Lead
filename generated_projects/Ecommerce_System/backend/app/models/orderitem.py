"""
OrderItem Model
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


class OrderItem(Base):

    __tablename__ = "orderitems"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    quantity = Column(
        Integer,
    )

    unit_price = Column(
        String,
    )
