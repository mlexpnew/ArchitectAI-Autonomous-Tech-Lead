```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///schedule.db"

# Create Database Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create Session Maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model
class Schedule(BaseModel):
    id: int
    name: str
    description: str

# Database Model
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScheduleDB(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# Create Database Tables
Base.metadata.create_all(engine)

# Repository Layer
class ScheduleRepository:
    def __init__(self, session: SessionLocal):
        self.session = session

    def get_all(self):
        return self.session.query(ScheduleDB).all()

    def get_by_id(self, id: int):
        return self.session.query(ScheduleDB).filter(ScheduleDB.id == id).first()

    def create(self, schedule: Schedule):
        db_schedule = ScheduleDB(name=schedule.name, description=schedule.description)
        self.session.add(db_schedule)
        self.session.commit()
        return db_schedule

    def update(self, id: int, schedule: Schedule):
        db_schedule = self.get_by_id(id)
        if db_schedule:
            db_schedule.name = schedule.name
            db_schedule.description = schedule.description
            self.session.commit()
            return db_schedule
        raise HTTPException(status_code=404, detail="Schedule not found")

    def delete(self, id: int):
        db_schedule = self.get_by_id(id)
        if db_schedule:
            self.session.delete(db_schedule)
            self.session.commit()
            return {"message": "Schedule deleted"}
        raise HTTPException(status_code=404, detail="Schedule not found")

# Service Layer
class ScheduleService:
    def __init__(self, repository: ScheduleRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, schedule: Schedule):
        return self.repository.create(schedule)

    def update(self, id: int, schedule: Schedule):
        return self.repository.update(id, schedule)

    def delete(self, id: int):
        return self.repository.delete(id)

# Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI App
app = FastAPI()

# Dependency Injection for Schedule Service
def get_schedule_service(db: SessionLocal = Depends(get_db)):
    return ScheduleService(ScheduleRepository(db))

# Endpoints
@app.get("/")
async def read_all(schedule_service: ScheduleService = Depends(get_schedule_service)):
    return schedule_service.get_all()

@app.get("/{id}")
async def read_by_id(id: int, schedule_service: ScheduleService = Depends(get_schedule_service)):
    return schedule_service.get_by_id(id)

@app.post("/")
async def create(schedule: Schedule, schedule_service: ScheduleService = Depends(get_schedule_service)):
    return schedule_service.create(schedule)

@app.put("/{id}")
async def update(id: int, schedule: Schedule, schedule_service: ScheduleService = Depends(get_schedule_service)):
    return schedule_service.update(id, schedule)

@app.delete("/{id}")
async def delete(id: int, schedule_service: ScheduleService = Depends(get_schedule_service)):
    return schedule_service.delete(id)
```

This code establishes a production-ready FastAPI CRUD Router for managing a Schedule entity. It utilizes the Repository Layer, Service Layer, and Dependency Injection to ensure a clean and maintainable architecture. The code is written in Python 3.12 and uses FastAPI, SQLAlchemy, and Pydantic V2.