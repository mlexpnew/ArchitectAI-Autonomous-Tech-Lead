```python
# patient_repository.py
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

class PatientRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, patient: PatientCreate) -> Patient:
        db_patient = Patient(
            name=patient.name,
            email=patient.email,
            phone_number=patient.phone_number
        )
        self.db_session.add(db_patient)
        self.db_session.commit()
        self.db_session.refresh(db_patient)
        return db_patient

    def get_all(self) -> List[Patient]:
        return self.db_session.query(Patient).all()

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.db_session.get(Patient, patient_id)

    def update(self, patient_id: int, patient: PatientUpdate) -> Patient:
        db_patient = self.get_by_id(patient_id)
        if db_patient:
            db_patient.name = patient.name
            db_patient.email = patient.email
            db_patient.phone_number = patient.phone_number
            self.db_session.commit()
            self.db_session.refresh(db_patient)
            return db_patient
        return None

    def delete(self, patient_id: int) -> None:
        db_patient = self.get_by_id(patient_id)
        if db_patient:
            self.db_session.delete(db_patient)
            self.db_session.commit()

# patient_service.py
from typing import List, Optional
from app.core.config import settings
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate

class PatientService:
    def __init__(self, db_session: Session):
        self.patient_repository = PatientRepository(db_session)

    def create(self, patient: PatientCreate) -> Patient:
        return self.patient_repository.create(patient)

    def get_all(self) -> List[Patient]:
        return self.patient_repository.get_all()

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.patient_repository.get_by_id(patient_id)

    def update(self, patient_id: int, patient: PatientUpdate) -> Patient:
        return self.patient_repository.update(patient_id, patient)

    def delete(self, patient_id: int) -> None:
        self.patient_repository.delete(patient_id)
```

```python
# __init__.py
from fastapi import FastAPI
from app.core.config import settings
from app.repositories.patient_repository import PatientRepository
from app.services.patient_service import PatientService

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    engine = settings.db_engine
    async with engine.begin() as conn:
        await conn.run_sync(settings.db_base.metadata.create_all)

    db_session = settings.db_session
    patient_service = PatientService(db_session)
    # Add patient_service to the app context
    app.state.patient_service = patient_service
```

```python
# main.py
from fastapi import FastAPI
from app import app

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
```

```python
# app/core/config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseSettings

class Settings(BaseSettings):
    db_url: str
    db_base: declarative_base()

    class Config:
        env_file = ".env"

settings = Settings()

db_engine = create_engine(settings.db_url)
settings.db_base.metadata.create_all(db_engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
```