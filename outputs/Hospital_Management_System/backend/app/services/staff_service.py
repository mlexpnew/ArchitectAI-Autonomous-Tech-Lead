```python
# staff_repository.py
from abc import ABC, abstractmethod
from typing import List

class StaffRepository(ABC):
    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> object:
        pass

    @abstractmethod
    def create(self, staff: object) -> object:
        pass

    @abstractmethod
    def update(self, id: int, staff: object) -> object:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
```

```python
# staff_repository_impl.py
from staff_repository import StaffRepository
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class StaffRepositoryImpl(StaffRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_all(self) -> List:
        return self.session.query(Staff).all()

    def get_by_id(self, id: int) -> object:
        return self.session.query(Staff).filter(Staff.id == id).first()

    def create(self, staff: object) -> object:
        self.session.add(staff)
        self.session.commit()
        return staff

    def update(self, id: int, staff: object) -> object:
        existing_staff = self.get_by_id(id)
        if existing_staff:
            existing_staff.name = staff.name
            existing_staff.email = staff.email
            self.session.commit()
        return existing_staff

    def delete(self, id: int) -> None:
        self.session.query(Staff).filter(Staff.id == id).delete()
        self.session.commit()
```

```python
# staff_service.py
from staff_repository import StaffRepository
from staff_repository_impl import StaffRepositoryImpl
from typing import List
from pydantic import BaseModel

class StaffRequest(BaseModel):
    name: str
    email: str

class StaffService:
    def __init__(self, repository: StaffRepository):
        self.repository = repository

    def get_all(self) -> List:
        return self.repository.get_all()

    def get_by_id(self, id: int) -> object:
        return self.repository.get_by_id(id)

    def create(self, staff_request: StaffRequest) -> object:
        staff = Staff(name=staff_request.name, email=staff_request.email)
        return self.repository.create(staff)

    def update(self, id: int, staff_request: StaffRequest) -> object:
        staff = self.repository.get_by_id(id)
        if staff:
            staff.name = staff_request.name
            staff.email = staff_request.email
            return self.repository.update(id, staff)
        return None

    def delete(self, id: int) -> None:
        self.repository.delete(id)
```

```python
# staff_validator.py
from pydantic import BaseModel, validator
from typing import Optional

class StaffRequest(BaseModel):
    name: str
    email: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Name must not be empty')
        return v

    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Email must be valid')
        return v
```

```python
# main.py
from staff_repository_impl import StaffRepositoryImpl
from staff_service import StaffService
from staff_validator import StaffRequest

def main():
    db_url = 'sqlite:///staff.db'
    repository = StaffRepositoryImpl(db_url)
    service = StaffService(repository)

    staff_request = StaffRequest(name='John Doe', email='john@example.com')
    staff = service.create(staff_request)
    print(staff)

    staff_request = StaffRequest(name='Jane Doe', email='jane@example.com')
    staff = service.create(staff_request)
    print(staff)

    staff = service.get_by_id(1)
    print(staff)

    staff_request = StaffRequest(name='John Doe', email='john@example.com')
    staff = service.update(1, staff_request)
    print(staff)

    service.delete(1)

if __name__ == '__main__':
    main()
```

This code defines a production-ready Service Layer for managing staff entities. It uses the Repository Pattern to encapsulate data access and the Service Layer to encapsulate business logic. The code also includes validation using Pydantic. The main.py file demonstrates how to use the Service Layer to create, read, update, and delete staff entities.