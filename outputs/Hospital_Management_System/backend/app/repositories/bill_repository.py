```python
# models/bill.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer)

    def __repr__(self):
        return f"Bill(id={self.id}, name='{self.name}', amount={self.amount})"

# repositories/bill_repository.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.bill import Bill, Base
from typing import List, Optional

class BillRepository:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create(self, bill: Bill) -> Bill:
        session = self.Session()
        session.add(bill)
        session.commit()
        return bill

    def get_all(self) -> List[Bill]:
        session = self.Session()
        return session.query(Bill).all()

    def get_by_id(self, id: int) -> Optional[Bill]:
        session = self.Session()
        return session.query(Bill).filter_by(id=id).first()

    def update(self, id: int, bill: Bill) -> Bill:
        session = self.Session()
        bill_to_update = session.query(Bill).filter_by(id=id).first()
        if bill_to_update:
            for key, value in bill.dict().items():
                setattr(bill_to_update, key, value)
            session.commit()
        return bill_to_update

    def delete(self, id: int) -> None:
        session = self.Session()
        bill_to_delete = session.query(Bill).filter_by(id=id).first()
        if bill_to_delete:
            session.delete(bill_to_delete)
            session.commit()

# repositories/__init__.py
from .bill_repository import BillRepository

def get_bill_repository(db_url: str) -> BillRepository:
    return BillRepository(db_url)
```

```python
# main.py
from repositories import get_bill_repository
from models.bill import Bill

if __name__ == "__main__":
    db_url = "sqlite:///example.db"
    bill_repository = get_bill_repository(db_url)

    # Create a new bill
    bill = Bill(name="Test Bill", amount=100)
    bill_repository.create(bill)

    # Get all bills
    bills = bill_repository.get_all()
    for bill in bills:
        print(bill)

    # Get a bill by id
    bill = bill_repository.get_by_id(1)
    print(bill)

    # Update a bill
    bill = bill_repository.get_by_id(1)
    bill.name = "Updated Test Bill"
    bill_repository.update(1, bill)

    # Delete a bill
    bill_repository.delete(1)
```