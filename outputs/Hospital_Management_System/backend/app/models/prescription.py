```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prescription(Base):
    __tablename__ = "prescriptions"

    id: int = Column(Integer, primary_key=True)
    patient_id: int = Column(Integer, nullable=False)
    doctor_id: int = Column(Integer, nullable=False)
    medicine: str = Column(String, nullable=False)
    dosage: str = Column(String, nullable=False)
    duration: str = Column(String, nullable=False)
```