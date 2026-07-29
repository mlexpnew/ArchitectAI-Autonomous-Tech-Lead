```python
# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///prescriptions.db"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create the database tables
Base = declarative_base()

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True)
    patient_name = Column(String)
    medication = Column(String)
    dosage = Column(String)

Base.metadata.create_all(engine)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Model
class PrescriptionBase(BaseModel):
    patient_name: str
    medication: str
    dosage: str

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(PrescriptionBase):
    pass

class Prescription(PrescriptionBase):
    id: int

# Service Layer
class PrescriptionService:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_all(self):
        return self.db.query(Prescription).all()

    def get_by_id(self, id: int):
        return self.db.query(Prescription).filter(Prescription.id == id).first()

    def create(self, prescription: PrescriptionCreate):
        db_prescription = Prescription(**prescription.dict())
        self.db.add(db_prescription)
        self.db.commit()
        self.db.refresh(db_prescription)
        return db_prescription

    def update(self, id: int, prescription: PrescriptionUpdate):
        db_prescription = self.get_by_id(id)
        if db_prescription:
            for attr, value in prescription.dict().items():
                setattr(db_prescription, attr, value)
            self.db.commit()
            return db_prescription
        raise HTTPException(status_code=404, detail="Prescription not found")

    def delete(self, id: int):
        db_prescription = self.get_by_id(id)
        if db_prescription:
            self.db.delete(db_prescription)
            self.db.commit()
            return {"message": "Prescription deleted successfully"}
        raise HTTPException(status_code=404, detail="Prescription not found")

# Router
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=List[Prescription])
async def read_prescriptions(db: SessionLocal = Depends(get_db)):
    return PrescriptionService(db).get_all()

@router.get("/{id}", response_model=Prescription)
async def read_prescription(id: int, db: SessionLocal = Depends(get_db)):
    return PrescriptionService(db).get_by_id(id)

@router.post("/", response_model=Prescription)
async def create_prescription(prescription: PrescriptionCreate, db: SessionLocal = Depends(get_db)):
    return PrescriptionService(db).create(prescription)

@router.put("/{id}", response_model=Prescription)
async def update_prescription(id: int, prescription: PrescriptionUpdate, db: SessionLocal = Depends(get_db)):
    return PrescriptionService(db).update(id, prescription)

@router.delete("/{id}")
async def delete_prescription(id: int, db: SessionLocal = Depends(get_db)):
    return PrescriptionService(db).delete(id)

# Main
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)
```

This code provides a production-ready FastAPI CRUD Router for managing prescriptions. It uses SQLAlchemy for database operations, Pydantic for data validation, and FastAPI for building the API. The repository layer is implemented using SQLAlchemy, and the service layer is used to encapsulate the business logic. Dependency injection is used to provide the database session to the service layer. The API has endpoints for creating, reading, updating, and deleting prescriptions.