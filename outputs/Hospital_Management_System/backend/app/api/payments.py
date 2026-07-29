```python
# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.services import PaymentService
from app.repositories import PaymentRepository
from app.dependencies import get_db

app = FastAPI()

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///payments.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    currency = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

# Pydantic Models
class PaymentBase(BaseModel):
    amount: int
    currency: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int

# Repository Layer
class PaymentRepository:
    def get_all(self, db: SessionLocal):
        return db.query(Payment).all()

    def get_by_id(self, db: SessionLocal, id: int):
        return db.query(Payment).filter(Payment.id == id).first()

    def create(self, db: SessionLocal, payment: PaymentCreate):
        db_payment = Payment(**payment.dict())
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment

    def update(self, db: SessionLocal, id: int, payment: PaymentCreate):
        db_payment = self.get_by_id(db, id)
        if db_payment:
            for attr, value in payment.dict().items():
                setattr(db_payment, attr, value)
            db.commit()
            db.refresh(db_payment)
            return db_payment
        raise HTTPException(status_code=404, detail="Payment not found")

    def delete(self, db: SessionLocal, id: int):
        db_payment = self.get_by_id(db, id)
        if db_payment:
            db.delete(db_payment)
            db.commit()
            return {"message": "Payment deleted successfully"}
        raise HTTPException(status_code=404, detail="Payment not found")

# Service Layer
class PaymentService:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def get_all(self, db: SessionLocal):
        return self.repository.get_all(db)

    def get_by_id(self, db: SessionLocal, id: int):
        return self.repository.get_by_id(db, id)

    def create(self, db: SessionLocal, payment: PaymentCreate):
        return self.repository.create(db, payment)

    def update(self, db: SessionLocal, id: int, payment: PaymentCreate):
        return self.repository.update(db, id, payment)

    def delete(self, db: SessionLocal, id: int):
        return self.repository.delete(db, id)

# Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/")
async def read_all(db: SessionLocal = Depends(get_db)):
    service = PaymentService(PaymentRepository())
    return service.get_all(db)

@app.get("/{id}")
async def read_by_id(id: int, db: SessionLocal = Depends(get_db)):
    service = PaymentService(PaymentRepository())
    return service.get_by_id(db, id)

@app.post("/")
async def create(payment: PaymentCreate, db: SessionLocal = Depends(get_db)):
    service = PaymentService(PaymentRepository())
    return service.create(db, payment)

@app.put("/{id}")
async def update(id: int, payment: PaymentCreate, db: SessionLocal = Depends(get_db)):
    service = PaymentService(PaymentRepository())
    return service.update(db, id, payment)

@app.delete("/{id}")
async def delete(id: int, db: SessionLocal = Depends(get_db)):
    service = PaymentService(PaymentRepository())
    return service.delete(db, id)
```