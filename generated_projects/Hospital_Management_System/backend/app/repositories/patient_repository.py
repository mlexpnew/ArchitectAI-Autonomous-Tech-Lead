"""
Patient Repository
"""

from sqlalchemy.orm import Session

from app.models.patient import Patient


class PatientRepository:

    @staticmethod
    def get_all(db: Session):

        return db.query(Patient).all()


    @staticmethod
    def get_by_id(
        db: Session,
        patient_id: int,
    ):

        return db.query(Patient).filter(
            Patient.id == patient_id
        ).first()


    @staticmethod
    def create(
        db: Session,
        patient: Patient,
    ):

        db.add(patient)

        db.commit()

        db.refresh(patient)

        return patient


    @staticmethod
    def delete(
        db: Session,
        patient_id: int,
    ):

        patient = db.query(Patient).filter(
            Patient.id == patient_id
        ).first()

        if patient:

            db.delete(patient)

            db.commit()

        return patient
