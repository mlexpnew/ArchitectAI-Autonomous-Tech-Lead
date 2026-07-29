```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Staff(Base):
    __tablename__ = "staff"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    phone: str = Column(String, nullable=False)
    address: str = Column(String, nullable=False)
```