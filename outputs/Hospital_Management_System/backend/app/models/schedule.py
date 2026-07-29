```python
from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(Date)
    time = Column(Time)
    status = Column(String)
    doctor = relationship("Doctor", backref="schedules")
```