```python
# repositories/staff_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.db import models
from app.db.database import async_session

class StaffRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, staff: models.Staff) -> models.Staff:
        async with self.session.begin():
            self.session.add(staff)
        return staff

    async def get_all(self) -> list[models.Staff]:
        query = select(models.Staff).options(selectinload(models.Staff.department))
        return await self.session.execute(query).all()

    async def get_by_id(self, staff_id: int) -> models.Staff | None:
        query = select(models.Staff).options(selectinload(models.Staff.department)).where(models.Staff.id == staff_id)
        return await self.session.execute(query).scalar_one_or_none()

    async def update(self, staff_id: int, staff: models.Staff) -> models.Staff:
        query = select(models.Staff).where(models.Staff.id == staff_id)
        existing_staff = await self.session.execute(query).scalar_one_or_none()
        if existing_staff:
            existing_staff.name = staff.name
            existing_staff.email = staff.email
            existing_staff.department_id = staff.department_id
            await self.session.commit()
            return existing_staff
        return None

    async def delete(self, staff_id: int):
        query = select(models.Staff).where(models.Staff.id == staff_id)
        existing_staff = await self.session.execute(query).scalar_one_or_none()
        if existing_staff:
            await self.session.delete(existing_staff)
            await self.session.commit()
```

```python
# services/staff_service.py
from typing import Optional
from app.repositories.staff_repository import StaffRepository

class StaffService:
    def __init__(self, staff_repository: StaffRepository):
        self.staff_repository = staff_repository

    async def create_staff(self, staff: models.Staff) -> models.Staff:
        return await self.staff_repository.create(staff)

    async def get_all_staff(self) -> list[models.Staff]:
        return await self.staff_repository.get_all()

    async def get_staff_by_id(self, staff_id: int) -> Optional[models.Staff]:
        return await self.staff_repository.get_by_id(staff_id)

    async def update_staff(self, staff_id: int, staff: models.Staff) -> Optional[models.Staff]:
        return await self.staff_repository.update(staff_id, staff)

    async def delete_staff(self, staff_id: int):
        await self.staff_repository.delete(staff_id)
```

```python
# main.py
from fastapi import FastAPI
from app.services.staff_service import StaffService
from app.repositories.staff_repository import StaffRepository

app = FastAPI()

async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()

@app.on_event("shutdown")
async def shutdown_event():
    await get_db().close()

@app.get("/staff/")
async def read_staff(db: AsyncSession = Depends(get_db)):
    staff_repository = StaffRepository(db)
    staff_service = StaffService(staff_repository)
    return await staff_service.get_all_staff()

@app.get("/staff/{staff_id}")
async def read_staff_by_id(staff_id: int, db: AsyncSession = Depends(get_db)):
    staff_repository = StaffRepository(db)
    staff_service = StaffService(staff_repository)
    return await staff_service.get_staff_by_id(staff_id)

@app.post("/staff/")
async def create_staff(staff: models.Staff, db: AsyncSession = Depends(get_db)):
    staff_repository = StaffRepository(db)
    staff_service = StaffService(staff_repository)
    return await staff_service.create_staff(staff)

@app.put("/staff/{staff_id}")
async def update_staff(staff_id: int, staff: models.Staff, db: AsyncSession = Depends(get_db)):
    staff_repository = StaffRepository(db)
    staff_service = StaffService(staff_repository)
    return await staff_service.update_staff(staff_id, staff)

@app.delete("/staff/{staff_id}")
async def delete_staff(staff_id: int, db: AsyncSession = Depends(get_db)):
    staff_repository = StaffRepository(db)
    staff_service = StaffService(staff_repository)
    return await staff_service.delete_staff(staff_id)
```