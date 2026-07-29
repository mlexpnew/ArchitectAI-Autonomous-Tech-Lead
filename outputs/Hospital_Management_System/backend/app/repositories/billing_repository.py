```python
# repository/billing_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from app.core.config import get_db
from app.models.billing import Billing

class BillingRepository:
    def __init__(self):
        self.session: Session = get_db()

    def create(self, billing: Billing) -> Billing:
        try:
            self.session.add(billing)
            self.session.commit()
            return billing
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def get_all(self) -> List[Billing]:
        try:
            return self.session.scalars(select(Billing)).all()
        except SQLAlchemyError as e:
            raise e

    def get_by_id(self, billing_id: int) -> Optional[Billing]:
        try:
            return self.session.get(Billing, billing_id)
        except SQLAlchemyError as e:
            raise e

    def update(self, billing_id: int, billing: Billing) -> Billing:
        try:
            billing_obj = self.get_by_id(billing_id)
            if billing_obj:
                billing_obj.__dict__.update(billing.__dict__)
                self.session.commit()
                return billing_obj
            else:
                raise ValueError("Billing not found")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def delete(self, billing_id: int) -> None:
        try:
            billing_obj = self.get_by_id(billing_id)
            if billing_obj:
                self.session.delete(billing_obj)
                self.session.commit()
            else:
                raise ValueError("Billing not found")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
```

```python
# app/core/config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# app/models/billing.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from typing import Optional

Base = declarative_base()

class Billing(Base):
    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    def __repr__(self):
        return f"Billing(id={self.id}, name='{self.name}', description='{self.description}')"
```