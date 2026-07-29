"""
Appointment Repository
"""

from sqlalchemy.orm import Session

from app.models.appointment import Appointment


class AppointmentRepository:

    @staticmethod
    def get_all(db: Session):

        return db.query(Appointment).all()
