```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from services import AppointmentService
from repositories import AppointmentRepository
from dependencies import get_db

Base = declarative_base()

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime, server_default=func.now())
    time = Column(String)

class AppointmentBase(BaseModel):
    name: str
    time: str

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class AppointmentInDB(AppointmentBase):
    id: int
    date: str

class AppointmentSchema(AppointmentInDB):
    pass

app = FastAPI()

engine = create_engine('sqlite:///appointments.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

@app.get("/")
async def read_appointments(db: SessionLocal = Depends(get_db)):
    return AppointmentRepository(db).get_all()

@app.get("/{id}")
async def read_appointment(id: int, db: SessionLocal = Depends(get_db)):
    return AppointmentRepository(db).get(id)

@app.post("/")
async def create_appointment(appointment: AppointmentCreate, db: SessionLocal = Depends(get_db)):
    return AppointmentService(db).create(appointment)

@app.put("/{id}")
async def update_appointment(id: int, appointment: AppointmentUpdate, db: SessionLocal = Depends(get_db)):
    return AppointmentService(db).update(id, appointment)

@app.delete("/{id}")
async def delete_appointment(id: int, db: SessionLocal = Depends(get_db)):
    return AppointmentService(db).delete(id)
```

```python
# services.py
from typing import List
from pydantic import BaseModel
from repositories import AppointmentRepository

class AppointmentService:
    def __init__(self, db):
        self.db = db

    def create(self, appointment: AppointmentCreate) -> AppointmentInDB:
        return AppointmentRepository(self.db).create(appointment)

    def update(self, id: int, appointment: AppointmentUpdate) -> AppointmentInDB:
        return AppointmentRepository(self.db).update(id, appointment)

    def delete(self, id: int) -> None:
        return AppointmentRepository(self.db).delete(id)
```

```python
# repositories.py
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

class AppointmentRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self) -> List[AppointmentInDB]:
        return self.db.query(Appointment).all()

    def get(self, id: int) -> AppointmentInDB:
        return self.db.query(Appointment).filter(Appointment.id == id).first()

    def create(self, appointment: AppointmentCreate) -> AppointmentInDB:
        db_appointment = Appointment(name=appointment.name, time=appointment.time)
        self.db.add(db_appointment)
        self.db.commit()
        self.db.refresh(db_appointment)
        return db_appointment

    def update(self, id: int, appointment: AppointmentUpdate) -> AppointmentInDB:
        db_appointment = self.get(id)
        if db_appointment:
            db_appointment.name = appointment.name
            db_appointment.time = appointment.time
            self.db.commit()
            self.db.refresh(db_appointment)
            return db_appointment
        else:
            raise HTTPException(status_code=404, detail="Appointment not found")

    def delete(self, id: int) -> None:
        db_appointment = self.get(id)
        if db_appointment:
            self.db.delete(db_appointment)
            self.db.commit()
        else:
            raise HTTPException(status_code=404, detail="Appointment not found")
```

```python
# dependencies.py
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This code sets up a FastAPI application with CRUD endpoints for appointments. It uses SQLAlchemy for database operations and Pydantic for data validation. The repository layer encapsulates database operations, and the service layer provides a higher-level interface for business logic. Dependency injection is used to provide the database session to the application.