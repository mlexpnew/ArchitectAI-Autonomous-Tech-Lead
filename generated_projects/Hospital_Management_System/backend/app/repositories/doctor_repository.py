"""
Doctor Repository
"""

from sqlalchemy.orm import Session

from app.models.doctor import Doctor


class DoctorRepository:

    @staticmethod
    def get_all(db: Session):

        return db.query(Doctor).all()
