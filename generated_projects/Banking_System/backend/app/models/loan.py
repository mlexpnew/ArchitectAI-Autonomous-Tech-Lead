"""
Loan Model
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


class Loan(Base):

    __tablename__ = "loans"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    loan_type = Column(
        String,
    )

    amount = Column(
        String,
    )

    interest_rate = Column(
        String,
    )

    tenure_months = Column(
        Integer,
    )

    status = Column(
        String,
    )
