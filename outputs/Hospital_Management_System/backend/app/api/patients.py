```python
# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List

# Database Settings
SQLALCHEMY_DATABASE_URL = "sqlite:///patient.db"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create the session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for declarative models
Base = declarative_base()

# FastAPI App
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Model
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"Patient(id={self.id}, name={self.name}, email={self.email})"

class PatientBase(BaseModel):
    name: str
    email: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class PatientInDB(PatientBase):
    id: int

# Repository Layer
class PatientRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_all(self):
        return self.db.query(Patient).all()

    def get_by_id(self, id: int):
        return self.db.query(Patient).filter(Patient.id == id).first()

    def create(self, patient: PatientCreate):
        db_patient = Patient(name=patient.name, email=patient.email)
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def update(self, id: int, patient: PatientUpdate):
        db_patient = self.get_by_id(id)
        if db_patient:
            db_patient.name = patient.name
            db_patient.email = patient.email
            self.db.commit()
            self.db.refresh(db_patient)
            return db_patient
        else:
            raise HTTPException(status_code=404, detail="Patient not found")

    def delete(self, id: int):
        db_patient = self.get_by_id(id)
        if db_patient:
            self.db.delete(db_patient)
            self.db.commit()
            return {"message": "Patient deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Patient not found")

# Service Layer
class PatientService:
    def __init__(self, repository: PatientRepository = Depends()):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, patient: PatientCreate):
        return self.repository.create(patient)

    def update(self, id: int, patient: PatientUpdate):
        return self.repository.update(id, patient)

    def delete(self, id: int):
        return self.repository.delete(id)

# Routes
@app.get("/")
async def read_all(db: SessionLocal = Depends(get_db)):
    service = PatientService(repository=PatientRepository(db))
    return service.get_all()

@app.get("/{id}")
async def read_by_id(id: int, db: SessionLocal = Depends(get_db)):
    service = PatientService(repository=PatientRepository(db))
    return service.get_by_id(id)

@app.post("/")
async def create(patient: PatientCreate, db: SessionLocal = Depends(get_db)):
    service = PatientService(repository=PatientRepository(db))
    return service.create(patient)

@app.put("/{id}")
async def update(id: int, patient: PatientUpdate, db: SessionLocal = Depends(get_db)):
    service = PatientService(repository=PatientRepository(db))
    return service.update(id, patient)

@app.delete("/{id}")
async def delete(id: int, db: SessionLocal = Depends(get_db)):
    service = PatientService(repository=PatientRepository(db))
    return service.delete(id)

# Create the tables
Base.metadata.create_all(engine)
```

This code defines a FastAPI CRUD router for the `Patient` entity. It uses the `SQLAlchemy` library for database operations and the `Pydantic` library for data validation. The `PatientRepository` class encapsulates the database operations, and the `PatientService` class provides a service layer for the repository. The `get_db` function is used to get a database session from the `SessionLocal` object.

The code includes the following routes:

*   `GET /`: Returns all patients.
*   `GET /{id}`: Returns a patient by ID.
*   `POST /`: Creates a new patient.
*   `PUT /{id}`: Updates a patient by ID.
*   `DELETE /{id}`: Deletes a patient by ID.

The code also includes the necessary database setup and table creation.

Note that this code assumes that you have the `fastapi`, `sqlalchemy`, and `pydantic` libraries installed in your project. You can install them using pip:

```bash
pip install fastapi sqlalchemy pydantic
```