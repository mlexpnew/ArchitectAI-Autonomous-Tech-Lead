```python
# service_layer/prescription_service.py

from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, validator
from repository_layer import prescription_repository

class Prescription(BaseModel):
    id: int
    patient_id: int
    medication_id: int
    dosage: str
    frequency: str

    @validator('dosage')
    def dosage_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Dosage cannot be empty')
        return v

    @validator('frequency')
    def frequency_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Frequency cannot be empty')
        return v


class PrescriptionRepository(ABC):
    @abstractmethod
    def get_all_prescriptions(self) -> List[Prescription]:
        pass

    @abstractmethod
    def get_prescription_by_id(self, id: int) -> Optional[Prescription]:
        pass

    @abstractmethod
    def create_prescription(self, prescription: Prescription) -> Prescription:
        pass

    @abstractmethod
    def update_prescription(self, id: int, prescription: Prescription) -> Prescription:
        pass

    @abstractmethod
    def delete_prescription(self, id: int) -> None:
        pass


class PrescriptionService:
    def __init__(self, repository: PrescriptionRepository):
        self.repository = repository

    def get_all_prescriptions(self) -> List[Prescription]:
        return self.repository.get_all_prescriptions()

    def get_prescription_by_id(self, id: int) -> Optional[Prescription]:
        return self.repository.get_prescription_by_id(id)

    def create_prescription(self, prescription: Prescription) -> Prescription:
        return self.repository.create_prescription(prescription)

    def update_prescription(self, id: int, prescription: Prescription) -> Prescription:
        return self.repository.update_prescription(id, prescription)

    def delete_prescription(self, id: int) -> None:
        self.repository.delete_prescription(id)


class PrescriptionRepositoryImpl(PrescriptionRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all_prescriptions(self) -> List[Prescription]:
        return [Prescription(**prescription) for prescription in self.db_session.query('prescriptions').all()]

    def get_prescription_by_id(self, id: int) -> Optional[Prescription]:
        prescription = self.db_session.query('prescriptions').filter_by(id=id).first()
        return Prescription(**prescription) if prescription else None

    def create_prescription(self, prescription: Prescription) -> Prescription:
        self.db_session.insert('prescriptions', prescription.dict())
        return prescription

    def update_prescription(self, id: int, prescription: Prescription) -> Prescription:
        self.db_session.update('prescriptions', id, prescription.dict())
        return prescription

    def delete_prescription(self, id: int) -> None:
        self.db_session.delete('prescriptions', id)


# Example usage:
if __name__ == '__main__':
    from repository_layer import db_session

    repository = PrescriptionRepositoryImpl(db_session)
    service = PrescriptionService(repository)

    # Create a new prescription
    prescription = Prescription(id=1, patient_id=1, medication_id=1, dosage='10mg', frequency='daily')
    created_prescription = service.create_prescription(prescription)
    print(created_prescription)

    # Get all prescriptions
    all_prescriptions = service.get_all_prescriptions()
    print(all_prescriptions)

    # Get a prescription by id
    prescription_by_id = service.get_prescription_by_id(1)
    print(prescription_by_id)

    # Update a prescription
    updated_prescription = Prescription(id=1, patient_id=1, medication_id=1, dosage='20mg', frequency='daily')
    updated_prescription = service.update_prescription(1, updated_prescription)
    print(updated_prescription)

    # Delete a prescription
    service.delete_prescription(1)
```

This code defines a production-ready Service Layer for managing prescriptions. It includes the following features:

*   **Business Logic**: The `PrescriptionService` class encapsulates the business logic for managing prescriptions, including creating, reading, updating, and deleting prescriptions.
*   **CRUD Operations**: The `PrescriptionService` class provides methods for performing CRUD (Create, Read, Update, Delete) operations on prescriptions.
*   **Validation**: The `Prescription` model uses Pydantic's validation features to ensure that prescription data is valid before creating or updating a prescription.
*   **Repository Pattern**: The `PrescriptionRepository` abstract base class defines the interface for interacting with the data storage, and the `PrescriptionRepositoryImpl` class provides a concrete implementation of the repository using a database session.

This code is designed to be flexible and scalable, making it suitable for use in a production environment.