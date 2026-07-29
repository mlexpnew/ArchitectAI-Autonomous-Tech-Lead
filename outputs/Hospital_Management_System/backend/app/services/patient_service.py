```python
# patient_service.py

from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime

class PatientRepository(ABC):
    @abstractmethod
    def get_all(self) -> List['Patient']:
        pass

    @abstractmethod
    def get_by_id(self, patient_id: int) -> Optional['Patient']:
        pass

    @abstractmethod
    def create(self, patient: 'Patient') -> 'Patient':
        pass

    @abstractmethod
    def update(self, patient_id: int, patient: 'Patient') -> 'Patient':
        pass

    @abstractmethod
    def delete(self, patient_id: int) -> None:
        pass


class Patient(BaseModel):
    id: int
    name: str
    date_of_birth: datetime
    address: str

    @validator('date_of_birth')
    def date_of_birth_must_be_in_the_past(cls, v):
        if v > datetime.now():
            raise ValueError('Date of birth must be in the past')
        return v

    class Config:
        orm_mode = True


class PatientService:
    def __init__(self, repository: PatientRepository):
        self.repository = repository

    def get_all(self) -> List[Patient]:
        return self.repository.get_all()

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.repository.get_by_id(patient_id)

    def create(self, patient: Patient) -> Patient:
        return self.repository.create(patient)

    def update(self, patient_id: int, patient: Patient) -> Patient:
        return self.repository.update(patient_id, patient)

    def delete(self, patient_id: int) -> None:
        self.repository.delete(patient_id)


class PatientRepositoryImpl(PatientRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all(self) -> List[Patient]:
        return self.db_session.query(Patient).all()

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.db_session.query(Patient).get(patient_id)

    def create(self, patient: Patient) -> Patient:
        self.db_session.add(patient)
        self.db_session.commit()
        return patient

    def update(self, patient_id: int, patient: Patient) -> Patient:
        existing_patient = self.get_by_id(patient_id)
        if existing_patient:
            existing_patient.name = patient.name
            existing_patient.date_of_birth = patient.date_of_birth
            existing_patient.address = patient.address
            self.db_session.commit()
            return existing_patient
        return None

    def delete(self, patient_id: int) -> None:
        patient = self.get_by_id(patient_id)
        if patient:
            self.db_session.delete(patient)
            self.db_session.commit()
```

```python
# main.py

from patient_service import PatientService, PatientRepositoryImpl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a database engine
engine = create_engine('sqlite:///patients.db')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Create a patient repository
repository = PatientRepositoryImpl(session)

# Create a patient service
service = PatientService(repository)

# Create a new patient
new_patient = Patient(name='John Doe', date_of_birth=datetime(1990, 1, 1), address='123 Main St')
new_patient = service.create(new_patient)

# Get all patients
patients = service.get_all()

# Print patients
for patient in patients:
    print(patient)

# Get a patient by id
patient = service.get_by_id(1)
print(patient)

# Update a patient
patient = service.get_by_id(1)
patient.name = 'Jane Doe'
service.update(1, patient)

# Delete a patient
service.delete(1)
```

This code defines a `Patient` entity with validation rules using Pydantic. It also defines a `PatientRepository` abstract base class with CRUD operations, and a concrete `PatientRepositoryImpl` class that uses SQLAlchemy to interact with a database. The `PatientService` class uses the repository to encapsulate business logic. The example use case in `main.py` demonstrates how to create a patient, get all patients, get a patient by id, update a patient, and delete a patient.