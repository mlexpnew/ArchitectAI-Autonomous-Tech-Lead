```python
# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.services import BillingService
from app.repositories import BillingRepository
from app.dependencies import get_db

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///billing.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Billing(Base):
    __tablename__ = "billings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"

Base.metadata.create_all(engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Repository
class BillingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Billing).all()

    def get_one(self, id: int):
        return self.db.query(Billing).filter(Billing.id == id).first()

    def create(self, billing: Billing):
        self.db.add(billing)
        self.db.commit()
        self.db.refresh(billing)
        return billing

    def update(self, id: int, billing: Billing):
        self.db.query(Billing).filter(Billing.id == id).update({
            Billing.name: billing.name,
            Billing.email: billing.email
        })
        self.db.commit()
        return self.db.query(Billing).filter(Billing.id == id).first()

    def delete(self, id: int):
        self.db.query(Billing).filter(Billing.id == id).delete()
        self.db.commit()

# Service
class BillingService:
    def __init__(self, repository: BillingRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_one(self, id: int):
        return self.repository.get_one(id)

    def create(self, billing: Billing):
        return self.repository.create(billing)

    def update(self, id: int, billing: Billing):
        return self.repository.update(id, billing)

    def delete(self, id: int):
        return self.repository.delete(id)

# Endpoints
@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    service = BillingService(BillingRepository(db))
    return service.get_all()

@app.get("/{id}")
async def read_one(id: int, db: Session = Depends(get_db)):
    service = BillingService(BillingRepository(db))
    return service.get_one(id)

@app.post("/")
async def create(billing: Billing, db: Session = Depends(get_db)):
    service = BillingService(BillingRepository(db))
    return service.create(billing)

@app.put("/{id}")
async def update(id: int, billing: Billing, db: Session = Depends(get_db)):
    service = BillingService(BillingRepository(db))
    return service.update(id, billing)

@app.delete("/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    service = BillingService(BillingRepository(db))
    return service.delete(id)
```

```python
# app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
```

```python
# app/repositories.py
from sqlalchemy.orm import Session
from app.models import Billing

class BillingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Billing).all()

    def get_one(self, id: int):
        return self.db.query(Billing).filter(Billing.id == id).first()

    def create(self, billing: Billing):
        self.db.add(billing)
        self.db.commit()
        self.db.refresh(billing)
        return billing

    def update(self, id: int, billing: Billing):
        self.db.query(Billing).filter(Billing.id == id).update({
            Billing.name: billing.name,
            Billing.email: billing.email
        })
        self.db.commit()
        return self.db.query(Billing).filter(Billing.id == id).first()

    def delete(self, id: int):
        self.db.query(Billing).filter(Billing.id == id).delete()
        self.db.commit()
```

```python
# app/services.py
from app.repositories import BillingRepository

class BillingService:
    def __init__(self, repository: BillingRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_one(self, id: int):
        return self.repository.get_one(id)

    def create(self, billing: Billing):
        return self.repository.create(billing)

    def update(self, id: int, billing: Billing):
        return self.repository.update(id, billing)

    def delete(self, id: int):
        return self.repository.delete(id)
```

```python
# app/models.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Billing(Base):
    __tablename__ = "billings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
```