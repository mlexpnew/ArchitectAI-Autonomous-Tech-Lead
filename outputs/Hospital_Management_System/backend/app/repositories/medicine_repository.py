```python
# models/medicine.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Medicine(Base):
    __tablename__ = 'medicines'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
```

```python
# repositories/medicine_repository.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Medicine

class MedicineRepository:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create(self, medicine: Medicine):
        session = self.Session()
        session.add(medicine)
        session.commit()
        return medicine

    def get_all(self):
        session = self.Session()
        return session.query(Medicine).all()

    def get_by_id(self, id: int):
        session = self.Session()
        return session.query(Medicine).filter(Medicine.id == id).first()

    def update(self, id: int, medicine: Medicine):
        session = self.Session()
        existing_medicine = session.query(Medicine).filter(Medicine.id == id).first()
        if existing_medicine:
            existing_medicine.name = medicine.name
            existing_medicine.description = medicine.description
            session.commit()
            return existing_medicine
        return None

    def delete(self, id: int):
        session = self.Session()
        medicine = session.query(Medicine).filter(Medicine.id == id).first()
        if medicine:
            session.delete(medicine)
            session.commit()
            return True
        return False
```

```python
# services/medicine_service.py
from repositories import medicine_repository

class MedicineService:
    def __init__(self, db_url: str):
        self.repository = medicine_repository.MedicineRepository(db_url)

    def create(self, medicine):
        return self.repository.create(medicine)

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def update(self, id, medicine):
        return self.repository.update(id, medicine)

    def delete(self, id):
        return self.repository.delete(id)
```

```python
# main.py
from services import medicine_service

if __name__ == '__main__':
    db_url = 'sqlite:///medicines.db'
    service = medicine_service.MedicineService(db_url)

    # Create
    medicine = medicine_service.Medicine(name='Aspirin', description='Pain reliever')
    created_medicine = service.create(medicine)
    print(created_medicine)

    # Get all
    all_medicines = service.get_all()
    for medicine in all_medicines:
        print(medicine)

    # Get by id
    medicine = service.get_by_id(1)
    print(medicine)

    # Update
    updated_medicine = service.update(1, medicine_service.Medicine(name='Ibuprofen', description='Pain reliever and anti-inflammatory'))
    print(updated_medicine)

    # Delete
    deleted = service.delete(1)
    print(deleted)
```