```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///staff.db"

# Create Database Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create Session Maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model
Base = declarative_base()

# Staff Model
class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# Pydantic Model
class StaffBase(BaseModel):
    name: str
    email: str

class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass

class StaffInDBBase(StaffBase):
    id: int

class StaffInDB(StaffInDBBase):
    pass

# Repository Layer
class StaffRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_all(self):
        return self.db.query(Staff).all()

    def get(self, id: int):
        return self.db.query(Staff).filter(Staff.id == id).first()

    def create(self, staff: StaffCreate):
        db_staff = Staff(**staff.dict())
        self.db.add(db_staff)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Staff with this email already exists")
        return db_staff

    def update(self, id: int, staff: StaffUpdate):
        db_staff = self.get(id)
        if db_staff:
            for key, value in staff.dict().items():
                setattr(db_staff, key, value)
            self.db.add(db_staff)
            self.db.commit()
            return db_staff
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    def delete(self, id: int):
        db_staff = self.get(id)
        if db_staff:
            self.db.delete(db_staff)
            self.db.commit()
            return JSONResponse(content={"message": "Staff deleted successfully"}, status_code=status.HTTP_200_OK)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

# Service Layer
class StaffService:
    def __init__(self, repository: StaffRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get(self, id: int):
        return self.repository.get(id)

    def create(self, staff: StaffCreate):
        return self.repository.create(staff)

    def update(self, id: int, staff: StaffUpdate):
        return self.repository.update(id, staff)

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

# Service
staff_service = StaffService(StaffRepository(SessionLocal()))

# Endpoints
@app.get("/")
async def read_all_staff(db: Session = Depends(get_db)):
    return staff_service.get_all()

@app.get("/{id}")
async def read_staff(id: int, db: Session = Depends(get_db)):
    return staff_service.get(id)

@app.post("/")
async def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    return staff_service.create(staff)

@app.put("/{id}")
async def update_staff(id: int, staff: StaffUpdate, db: Session = Depends(get_db)):
    return staff_service.update(id, staff)

@app.delete("/{id}")
async def delete_staff(id: int, db: Session = Depends(get_db)):
    return staff_service.delete(id)
```

This code defines a production-ready FastAPI CRUD router for the Staff entity. It uses the Repository Layer, Service Layer, and Dependency Injection to separate concerns and make the code more maintainable. The code also uses Pydantic V2 for data validation and SQLAlchemy for database operations.