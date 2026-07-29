```python
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, nullable=False)
    medicine_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
```