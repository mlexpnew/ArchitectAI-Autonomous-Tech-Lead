```python
# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List

from app.config import settings
from app.routers import medicine_router
from app.services import MedicineService
from app.repositories import MedicineRepository

app = FastAPI()

# Database Connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Medicine Model
class Medicine(BaseModel):
    id: int
    name: str
    description: str

# Medicine Service
class MedicineService:
    def __init__(self, repository: MedicineRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, medicine: Medicine):
        return self.repository.create(medicine)

    def update(self, id: int, medicine: Medicine):
        return self.repository.update(id, medicine)

    def delete(self, id: int):
        return self.repository.delete(id)

# Medicine Repository
class MedicineRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_all(self):
        return self.db.query(Medicine).all()

    def get_by_id(self, id: int):
        return self.db.query(Medicine).filter(Medicine.id == id).first()

    def create(self, medicine: Medicine):
        self.db.add(medicine)
        self.db.commit()
        self.db.refresh(medicine)
        return medicine

    def update(self, id: int, medicine: Medicine):
        existing_medicine = self.get_by_id(id)
        if existing_medicine:
            existing_medicine.name = medicine.name
            existing_medicine.description = medicine.description
            self.db.commit()
            self.db.refresh(existing_medicine)
            return existing_medicine
        raise HTTPException(status_code=404, detail="Medicine not found")

    def delete(self, id: int):
        self.db.query(Medicine).filter(Medicine.id == id).delete()
        self.db.commit()
        return True

# Dependency Injection
@app.api_route("/")
async def read_root():
    return {"message": "Hello World"}

@app.api_route("/medicine", methods=["GET"])
async def read_medicine(db: SessionLocal = Depends(get_db), service: MedicineService = Depends(MedicineService)):
    return service.get_all()

@app.api_route("/medicine/{id}", methods=["GET"])
async def read_medicine_by_id(id: int, db: SessionLocal = Depends(get_db), service: MedicineService = Depends(MedicineService)):
    return service.get_by_id(id)

@app.api_route("/medicine", methods=["POST"])
async def create_medicine(medicine: Medicine, db: SessionLocal = Depends(get_db), service: MedicineService = Depends(MedicineService)):
    return service.create(medicine)

@app.api_route("/medicine/{id}", methods=["PUT"])
async def update_medicine(id: int, medicine: Medicine, db: SessionLocal = Depends(get_db), service: MedicineService = Depends(MedicineService)):
    return service.update(id, medicine)

@app.api_route("/medicine/{id}", methods=["DELETE"])
async def delete_medicine(id: int, db: SessionLocal = Depends(get_db), service: MedicineService = Depends(MedicineService)):
    return service.delete(id)

# Router
app.include_router(medicine_router)
```

```python
# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
```

```python
# app/routers.py
from fastapi import APIRouter
from app.services import MedicineService

medicine_router = APIRouter()

# Dependency Injection
@medicine_router.api_route("/medicine", methods=["GET"])
async def read_medicine(service: MedicineService = Depends(MedicineService)):
    return service.get_all()

@medicine_router.api_route("/medicine/{id}", methods=["GET"])
async def read_medicine_by_id(id: int, service: MedicineService = Depends(MedicineService)):
    return service.get_by_id(id)

@medicine_router.api_route("/medicine", methods=["POST"])
async def create_medicine(medicine: Medicine, service: MedicineService = Depends(MedicineService)):
    return service.create(medicine)

@medicine_router.api_route("/medicine/{id}", methods=["PUT"])
async def update_medicine(id: int, medicine: Medicine, service: MedicineService = Depends(MedicineService)):
    return service.update(id, medicine)

@medicine_router.api_route("/medicine/{id}", methods=["DELETE"])
async def delete_medicine(id: int, service: MedicineService = Depends(MedicineService)):
    return service.delete(id)
```

```python
# app/services.py
from app.repositories import MedicineRepository

class MedicineService:
    def __init__(self, repository: MedicineRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, medicine: Medicine):
        return self.repository.create(medicine)

    def update(self, id: int, medicine: Medicine):
        return self.repository.update(id, medicine)

    def delete(self, id: int):
        return self.repository.delete(id)
```

```python
# app/repositories.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List

from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Medicine(BaseModel):
    id: int
    name: str
    description: str

class MedicineRepository:
    def __init__(self, db: SessionLocal):
        self.db = db

    def get_all(self):
        return self.db.query(Medicine).all()

    def get_by_id(self, id: int):
        return self.db.query(Medicine).filter(Medicine.id == id).first()

    def create(self, medicine: Medicine):
        self.db.add(medicine)
        self.db.commit()
        self.db.refresh(medicine)
        return medicine

    def update(self, id: int, medicine: Medicine):
        existing_medicine = self.get_by_id(id)
        if existing_medicine:
            existing_medicine.name = medicine.name
            existing_medicine.description = medicine.description
            self.db.commit()
            self.db.refresh(existing_medicine)
            return existing_medicine
        raise Exception("Medicine not found")

    def delete(self, id: int):
        self.db.query(Medicine).filter(Medicine.id == id).delete()
        self.db.commit()
        return True
```