"""
Patient API
"""

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.patient import (
    PatientCreate,
    PatientResponse,
)

from app.services.patient_service import PatientService

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


@router.get(
    "/",
    response_model=list[PatientResponse],
)
def get_patients(
    db: Session = Depends(get_db),
):

    return PatientService.get_all(db)


@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
):

    return PatientService.get_by_id(
        db,
        patient_id,
    )


@router.post(
    "/",
    response_model=PatientResponse,
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
):

    return PatientService.create(
        db,
        patient,
    )


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
):

    PatientService.delete(
        db,
        patient_id,
    )

    return {
        "message": "Patient deleted"
    }
