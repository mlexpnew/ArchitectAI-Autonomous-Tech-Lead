```python
from sqlalchemy import Column, Integer, Date, Time, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

Base: declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String, nullable=False, default="pending")
```