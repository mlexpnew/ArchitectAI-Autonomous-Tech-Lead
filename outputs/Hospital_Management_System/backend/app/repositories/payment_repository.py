```python
# repositories/payment_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List, Optional

from models.payment import Payment
from core.config import settings

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create(self, payment: Payment) -> Payment:
        async with self.db.begin() as session:
            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return payment

    async def get_all(self) -> List[Payment]:
        async with self.db.begin() as session:
            result = await session.execute(select(Payment))
            return result.scalars().all()

    async def get_by_id(self, id: int) -> Optional[Payment]:
        async with self.db.begin() as session:
            result = await session.execute(select(Payment).where(Payment.id == id))
            return result.scalars().first()

    async def update(self, id: int, payment: Payment) -> Payment:
        async with self.db.begin() as session:
            await session.execute(
                select(Payment).where(Payment.id == id).update(payment.dict(exclude_unset=True))
            )
            await session.commit()
            result = await session.execute(select(Payment).where(Payment.id == id))
            return result.scalars().first()

    async def delete(self, id: int) -> None:
        async with self.db.begin() as session:
            await session.execute(select(Payment).where(Payment.id == id).delete())
            await session.commit()


# repositories/__init__.py
from .payment_repository import PaymentRepository
```

```python
# models/payment.py
from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class Payment(BaseModel):
    id: int
    amount: float
    currency: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
```

```python
# core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

```python
# main.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings
from repositories.payment_repository import PaymentRepository

engine = create_async_engine(settings.database_url)
async_session = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
    bind=engine,
)

async def main():
    async with async_session() as session:
        payment_repository = PaymentRepository(session)
        payment = Payment(id=1, amount=100.0, currency="USD", created_at=datetime.now(), updated_at=datetime.now())
        payment = await payment_repository.create(payment)
        print(payment)
        payments = await payment_repository.get_all()
        print(payments)
        payment = await payment_repository.get_by_id(1)
        print(payment)
        payment = Payment(id=1, amount=200.0, currency="USD", created_at=datetime.now(), updated_at=datetime.now())
        payment = await payment_repository.update(1, payment)
        print(payment)
        await payment_repository.delete(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```