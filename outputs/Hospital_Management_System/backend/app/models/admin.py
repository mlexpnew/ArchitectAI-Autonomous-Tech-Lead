```python
from sqlalchemy import Column, Integer, String, Password, ForeignKey
from sqlalchemy.orm import declarative_base
from typing import Optional

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(Password, nullable=False)
```