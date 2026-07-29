```python
from sqlalchemy import Column, Integer, Decimal, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bill(Base):
    __tablename__ = "bills"

    id: int = Column(Integer, primary_key=True)
    patient_id: int = Column(Integer, nullable=False)
    amount: float = Column(Decimal, nullable=False)
    payment_status: str = Column(String, nullable=False)
    date: date = Column(Date, nullable=False)
```