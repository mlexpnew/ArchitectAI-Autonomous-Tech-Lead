```python
# repositories/admin_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.config import settings
from app.db import database
from app.models.admin import Admin

class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, admin: Admin) -> Admin:
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    def get_all(self) -> List[Admin]:
        query = select(Admin)
        return self.db.scalars(query).all()

    def get_by_id(self, id: int) -> Optional[Admin]:
        query = select(Admin).where(Admin.id == id)
        return self.db.scalars(query).first()

    def update(self, id: int, admin: Admin) -> Admin:
        existing_admin = self.get_by_id(id)
        if existing_admin:
            existing_admin.name = admin.name
            existing_admin.email = admin.email
            self.db.commit()
            self.db.refresh(existing_admin)
            return existing_admin
        return None

    def delete(self, id: int) -> bool:
        query = select(Admin).where(Admin.id == id)
        admin = self.db.scalars(query).first()
        if admin:
            self.db.delete(admin)
            self.db.commit()
            return True
        return False
```

```python
# app/services/admin_service.py
from app.repositories.admin_repository import AdminRepository

class AdminService:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def create_admin(self, admin: Admin) -> Admin:
        return self.admin_repository.create(admin)

    def get_all_admins(self) -> List[Admin]:
        return self.admin_repository.get_all()

    def get_admin_by_id(self, id: int) -> Optional[Admin]:
        return self.admin_repository.get_by_id(id)

    def update_admin(self, id: int, admin: Admin) -> Admin:
        return self.admin_repository.update(id, admin)

    def delete_admin(self, id: int) -> bool:
        return self.admin_repository.delete(id)
```

```python
# app/main.py
from fastapi import FastAPI
from app.services.admin_service import AdminService
from app.repositories.admin_repository import AdminRepository

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    engine = database.engine
    async with engine.begin() as conn:
        await conn.run_migrations()

@app.get("/admins/")
async def read_admins(admin_service: AdminService = Depends()):
    return admin_service.get_all_admins()

@app.get("/admins/{admin_id}")
async def read_admin(admin_id: int, admin_service: AdminService = Depends()):
    return admin_service.get_admin_by_id(admin_id)

@app.post("/admins/")
async def create_admin(admin: Admin, admin_service: AdminService = Depends()):
    return admin_service.create_admin(admin)

@app.put("/admins/{admin_id}")
async def update_admin(admin_id: int, admin: Admin, admin_service: AdminService = Depends()):
    return admin_service.update_admin(admin_id, admin)

@app.delete("/admins/{admin_id}")
async def delete_admin(admin_id: int, admin_service: AdminService = Depends()):
    return admin_service.delete_admin(admin_id)
```

```python
# app/models/admin.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

```python
# app/db/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, class_=AsyncSession, expire_on_commit=False, bind=engine)
```

```python
# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
```

```python
# .env
DATABASE_URL="sqlite+aiosqlite:///database.db"
```