```python
# medicine_repository.py
from abc import ABC, abstractmethod
from typing import List

class MedicineRepository(ABC):
    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> object:
        pass

    @abstractmethod
    def create(self, medicine: object) -> object:
        pass

    @abstractmethod
    def update(self, id: int, medicine: object) -> object:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
```

```python
# medicine_repository_impl.py
from abc import ABC, abstractmethod
from typing import List
from medicine_repository import MedicineRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///medicine.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Medicine(Base):
    __tablename__ = 'medicine'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

class MedicineRepositoryImpl(MedicineRepository):
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def get_all(self) -> List:
        return self.session.query(Medicine).all()

    def get_by_id(self, id: int) -> object:
        return self.session.query(Medicine).filter(Medicine.id == id).first()

    def create(self, medicine: object) -> object:
        self.session.add(medicine)
        self.session.commit()
        return medicine

    def update(self, id: int, medicine: object) -> object:
        existing_medicine = self.get_by_id(id)
        if existing_medicine:
            existing_medicine.name = medicine.name
            existing_medicine.description = medicine.description
            self.session.commit()
            return existing_medicine
        return None

    def delete(self, id: int) -> None:
        self.session.query(Medicine).filter(Medicine.id == id).delete()
        self.session.commit()
```

```python
# medicine_service.py
from abc import ABC, abstractmethod
from typing import List
from medicine_repository import MedicineRepository
from medicine_repository_impl import MedicineRepositoryImpl
from pydantic import BaseModel

class MedicineBase(BaseModel):
    name: str
    description: str

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(MedicineBase):
    pass

class MedicineService(ABC):
    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> object:
        pass

    @abstractmethod
    def create(self, medicine: MedicineCreate) -> object:
        pass

    @abstractmethod
    def update(self, id: int, medicine: MedicineUpdate) -> object:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

class MedicineServiceImpl(MedicineService):
    def __init__(self, repository: MedicineRepository):
        self.repository = repository

    def get_all(self) -> List:
        return self.repository.get_all()

    def get_by_id(self, id: int) -> object:
        return self.repository.get_by_id(id)

    def create(self, medicine: MedicineCreate) -> object:
        return self.repository.create(medicine)

    def update(self, id: int, medicine: MedicineUpdate) -> object:
        return self.repository.update(id, medicine)

    def delete(self, id: int) -> None:
        self.repository.delete(id)
```

```python
# main.py
from medicine_service import MedicineServiceImpl
from medicine_repository_impl import MedicineRepositoryImpl
from pydantic import ValidationError
from typing import List

repository = MedicineRepositoryImpl()
service = MedicineServiceImpl(repository)

# Create
medicine = service.create(MedicineCreate(name='Aspirin', description='Pain reliever'))
print(medicine)

# Get all
medicines = service.get_all()
print(medicines)

# Get by id
medicine = service.get_by_id(1)
print(medicine)

# Update
medicine = service.update(1, MedicineUpdate(name='Ibuprofen', description='Pain reliever'))
print(medicine)

# Delete
service.delete(1)
```

```python
# validation.py
from pydantic import BaseModel, validator
from typing import List

class MedicineBase(BaseModel):
    name: str
    description: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Name must not be empty')
        return v

    @validator('description')
    def description_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Description must not be empty')
        return v
```

```python
# business_logic.py
from typing import List
from medicine_repository import MedicineRepository

class MedicineBusinessLogic:
    def __init__(self, repository: MedicineRepository):
        self.repository = repository

    def get_all(self) -> List:
        return self.repository.get_all()

    def get_by_id(self, id: int) -> object:
        return self.repository.get_by_id(id)

    def create(self, medicine: object) -> object:
        return self.repository.create(medicine)

    def update(self, id: int, medicine: object) -> object:
        return self.repository.update(id, medicine)

    def delete(self, id: int) -> None:
        self.repository.delete(id)
```