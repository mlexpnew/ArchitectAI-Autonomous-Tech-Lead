```python
# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
from app.services import BillService
from app.repositories import BillRepository
from app.dependencies import get_db

app = FastAPI()

engine = create_engine("sqlite:///bills.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Bill(BaseModel):
    id: int
    description: str
    amount: float

@app.get("/")
async def read_bills(db: SessionLocal = Depends(get_db)):
    return BillService(db).get_all_bills()

@app.get("/{id}", response_model=Bill)
async def read_bill(id: int, db: SessionLocal = Depends(get_db)):
    return BillService(db).get_bill(id)

@app.post("/")
async def create_bill(bill: Bill, db: SessionLocal = Depends(get_db)):
    return BillService(db).create_bill(bill)

@app.put("/{id}")
async def update_bill(id: int, bill: Bill, db: SessionLocal = Depends(get_db)):
    return BillService(db).update_bill(id, bill)

@app.delete("/{id}")
async def delete_bill(id: int, db: SessionLocal = Depends(get_db)):
    return BillService(db).delete_bill(id)

class BillRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_all_bills(self):
        return self.db.query(Bill).all()

    def get_bill(self, id: int):
        return self.db.query(Bill).filter(Bill.id == id).first()

    def create_bill(self, bill: Bill):
        self.db.add(bill)
        self.db.commit()
        self.db.refresh(bill)
        return bill

    def update_bill(self, id: int, bill: Bill):
        self.db.query(Bill).filter(Bill.id == id).update(bill)
        self.db.commit()
        return bill

    def delete_bill(self, id: int):
        self.db.query(Bill).filter(Bill.id == id).delete()
        self.db.commit()

class BillService:
    def __init__(self, db: SessionLocal):
        self.db = db
        self.repository = BillRepository(db)

    def get_all_bills(self):
        return self.repository.get_all_bills()

    def get_bill(self, id: int):
        return self.repository.get_bill(id)

    def create_bill(self, bill: Bill):
        return self.repository.create_bill(bill)

    def update_bill(self, id: int, bill: Bill):
        return self.repository.update_bill(id, bill)

    def delete_bill(self, id: int):
        return self.repository.delete_bill(id)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# app/services.py
from app.repositories import BillRepository

class BillService:
    def __init__(self, db: SessionLocal):
        self.db = db
        self.repository = BillRepository(db)
```

```python
# app/repositories.py
from app.models import Bill

class BillRepository:
    def __init__(self, db: SessionLocal):
        self.db = db
```

```python
# app/models.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
```

```python
# app/config.py
from sqlalchemy import create_engine

engine = create_engine("sqlite:///bills.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

```python
# requirements.txt
fastapi==0.95.1
sqlalchemy==1.4.39
pydantic==2.1.12
```