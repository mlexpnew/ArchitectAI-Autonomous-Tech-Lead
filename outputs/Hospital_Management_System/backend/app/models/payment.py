```python
from sqlalchemy import Column, Integer, Numeric, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"

    id: int = Column(Integer, primary_key=True)
    patient_id: int = Column(Integer, nullable=False)
    amount: float = Column(Numeric(precision=10, scale=2), nullable=False)
    payment_method: str = Column(String(50), nullable=False)
    date: date = Column(Date, nullable=False)
```