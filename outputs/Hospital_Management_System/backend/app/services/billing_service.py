```python
# service_layer/billing.py
from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, validator
from repository_layer import BillingRepository

class BillingBase(BaseModel):
    id: Optional[int]
    customer_id: int
    invoice_date: str
    total_amount: float

    @validator('total_amount')
    def total_amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Total amount must be positive')
        return v

class BillingCreate(BillingBase):
    pass

class BillingUpdate(BillingBase):
    pass

class BillingService(ABC):
    def __init__(self, repository: BillingRepository):
        self.repository = repository

    @abstractmethod
    def get(self, id: int) -> Optional[BillingBase]:
        pass

    @abstractmethod
    def create(self, billing: BillingCreate) -> BillingBase:
        pass

    @abstractmethod
    def update(self, id: int, billing: BillingUpdate) -> BillingBase:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

class BillingServiceImpl(BillingService):
    def get(self, id: int) -> Optional[BillingBase]:
        return self.repository.get(id)

    def create(self, billing: BillingCreate) -> BillingBase:
        return self.repository.create(billing)

    def update(self, id: int, billing: BillingUpdate) -> BillingBase:
        return self.repository.update(id, billing)

    def delete(self, id: int) -> None:
        self.repository.delete(id)
```

```python
# repository_layer/billing_repository.py
from abc import ABC, abstractmethod
from typing import Optional

class BillingRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional:
        pass

    @abstractmethod
    def create(self, billing: object) -> object:
        pass

    @abstractmethod
    def update(self, id: int, billing: object) -> object:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
```

```python
# repository_layer/sqlalchemy_billing_repository.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from typing import Optional
from repository_layer.billing_repository import BillingRepository
from service_layer.billing import BillingBase

Base = declarative_base()

class Billing(Base):
    __tablename__ = 'billings'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    invoice_date = Column(String)
    total_amount = Column(Float)

class SQLAlchemyBillingRepository(BillingRepository):
    def __init__(self, db_url: str):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get(self, id: int) -> Optional[BillingBase]:
        billing = self.session.query(Billing).get(id)
        return billing

    def create(self, billing: BillingBase) -> BillingBase:
        new_billing = Billing(**billing.dict())
        self.session.add(new_billing)
        self.session.commit()
        return new_billing

    def update(self, id: int, billing: BillingBase) -> BillingBase:
        existing_billing = self.session.query(Billing).get(id)
        if existing_billing:
            for key, value in billing.dict().items():
                setattr(existing_billing, key, value)
            self.session.commit()
        return existing_billing

    def delete(self, id: int) -> None:
        billing = self.session.query(Billing).get(id)
        if billing:
            self.session.delete(billing)
            self.session.commit()
```

```python
# main.py
from service_layer.billing import BillingServiceImpl
from repository_layer.sqlalchemy_billing_repository import SQLAlchemyBillingRepository

if __name__ == '__main__':
    db_url = 'sqlite:///billing.db'
    repository = SQLAlchemyBillingRepository(db_url)
    service = BillingServiceImpl(repository)

    # Create a new billing
    billing = BillingCreate(customer_id=1, invoice_date='2022-01-01', total_amount=100.0)
    new_billing = service.create(billing)
    print(new_billing)

    # Get a billing by id
    billing = service.get(1)
    print(billing)

    # Update a billing
    billing = BillingUpdate(id=1, customer_id=2, invoice_date='2022-01-02', total_amount=200.0)
    updated_billing = service.update(1, billing)
    print(updated_billing)

    # Delete a billing
    service.delete(1)
```

This code implements a production-ready Service Layer using the Repository Pattern. It includes business logic, CRUD operations, validation, and a SQLAlchemy repository. The `BillingServiceImpl` class provides a concrete implementation of the `BillingService` interface, and the `SQLAlchemyBillingRepository` class provides a concrete implementation of the `BillingRepository` interface. The `main.py` file demonstrates how to use the Service Layer to create, read, update, and delete billings.