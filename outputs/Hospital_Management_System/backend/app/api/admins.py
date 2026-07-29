```python
# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
from app.repository.admin_repository import AdminRepository
from app.service.admin_service import AdminService

SQLALCHEMY_DATABASE_URL = "sqlite:///admin.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(engine)

class AdminBase(BaseModel):
    name: str
    email: str

class AdminCreate(AdminBase):
    pass

class AdminUpdate(AdminBase):
    pass

class AdminInDBBase(AdminBase):
    id: int

class Admin(AdminInDBBase):
    pass

class AdminDB(AdminInDBBase):
    name: str
    email: str

class AdminService:
    def __init__(self, repository: AdminRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, admin: AdminCreate):
        return self.repository.create(admin)

    def update(self, id: int, admin: AdminUpdate):
        return self.repository.update(id, admin)

    def delete(self, id: int):
        return self.repository.delete(id)

class AdminRepository:
    def __init__(self, session: SessionLocal):
        self.session = session

    def get_all(self):
        return self.session.query(Admin).all()

    def get_by_id(self, id: int):
        return self.session.query(Admin).get(id)

    def create(self, admin: AdminCreate):
        db_admin = Admin(name=admin.name, email=admin.email)
        self.session.add(db_admin)
        self.session.commit()
        self.session.refresh(db_admin)
        return db_admin

    def update(self, id: int, admin: AdminUpdate):
        db_admin = self.get_by_id(id)
        if db_admin:
            db_admin.name = admin.name
            db_admin.email = admin.email
            self.session.commit()
            self.session.refresh(db_admin)
            return db_admin
        return None

    def delete(self, id: int):
        db_admin = self.get_by_id(id)
        if db_admin:
            self.session.delete(db_admin)
            self.session.commit()
            return True
        return False

@app.get("/")
async def read_all(admin_service: AdminService = Depends()):
    return admin_service.get_all()

@app.get("/{id}")
async def read_by_id(id: int, admin_service: AdminService = Depends()):
    return admin_service.get_by_id(id)

@app.post("/")
async def create(admin: AdminCreate, admin_service: AdminService = Depends()):
    return admin_service.create(admin)

@app.put("/{id}")
async def update(id: int, admin: AdminUpdate, admin_service: AdminService = Depends()):
    return admin_service.update(id, admin)

@app.delete("/{id}")
async def delete(id: int, admin_service: AdminService = Depends()):
    return admin_service.delete(id)
```

```python
# app/repository/admin_repository.py
from sqlalchemy.orm import Session
from app.models import Admin

class AdminRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Admin).all()

    def get_by_id(self, id: int):
        return self.session.query(Admin).get(id)

    def create(self, admin: Admin):
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)
        return admin

    def update(self, id: int, admin: Admin):
        db_admin = self.get_by_id(id)
        if db_admin:
            db_admin.name = admin.name
            db_admin.email = admin.email
            self.session.commit()
            self.session.refresh(db_admin)
            return db_admin
        return None

    def delete(self, id: int):
        db_admin = self.get_by_id(id)
        if db_admin:
            self.session.delete(db_admin)
            self.session.commit()
            return True
        return False
```

```python
# app/service/admin_service.py
from app.repository.admin_repository import AdminRepository

class AdminService:
    def __init__(self, repository: AdminRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, admin: object):
        return self.repository.create(admin)

    def update(self, id: int, admin: object):
        return self.repository.update(id, admin)

    def delete(self, id: int):
        return self.repository.delete(id)
```

```python
# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```