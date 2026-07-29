```python
# repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.domain import models
from app.domain.models import Prescription
from app.infrastructure.database import database

class PrescriptionRepository:
    def __init__(self, session: Session | AsyncSession):
        self.session = session

    async def create(self, prescription: Prescription) -> Prescription:
        async with self.session.begin():
            db_prescription = Prescription(**prescription.dict())
            self.session.add(db_prescription)
            await self.session.commit()
            await self.session.refresh(db_prescription)
            return db_prescription

    async def get_all(self) -> list[Prescription]:
        query = select(Prescription)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Prescription | None:
        query = select(Prescription).where(Prescription.id == id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, id: int, prescription: Prescription) -> Prescription:
        query = select(Prescription).where(Prescription.id == id)
        result = await self.session.execute(query)
        db_prescription = result.scalars().first()
        if db_prescription:
            for attr, value in prescription.dict().items():
                setattr(db_prescription, attr, value)
            await self.session.commit()
            await self.session.refresh(db_prescription)
            return db_prescription
        return None

    async def delete(self, id: int) -> None:
        query = select(Prescription).where(Prescription.id == id)
        result = await self.session.execute(query)
        db_prescription = result.scalars().first()
        if db_prescription:
            await self.session.delete(db_prescription)
            await self.session.commit()
```

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///database.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
```

```python
# main.py
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from repository import PrescriptionRepository

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///database.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

prescription_repository = PrescriptionRepository(get_db())

@app.post("/prescriptions/")
async def create_prescription(prescription: Prescription):
    return await prescription_repository.create(prescription)

@app.get("/prescriptions/")
async def get_all_prescriptions():
    return await prescription_repository.get_all()

@app.get("/prescriptions/{id}")
async def get_prescription(id: int):
    return await prescription_repository.get_by_id(id)

@app.put("/prescriptions/{id}")
async def update_prescription(id: int, prescription: Prescription):
    return await prescription_repository.update(id, prescription)

@app.delete("/prescriptions/{id}")
async def delete_prescription(id: int):
    return await prescription_repository.delete(id)
```