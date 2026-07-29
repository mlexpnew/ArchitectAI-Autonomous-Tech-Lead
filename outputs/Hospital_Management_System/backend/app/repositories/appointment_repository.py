```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///appointments.db"

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

# Appointment Model
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String, index=True)
    time = Column(String, index=True)

    def __repr__(self):
        return f"Appointment(id={self.id}, name='{self.name}', date='{self.date}', time='{self.time}')"

# Repository Interface
class AppointmentRepository:
    def __init__(self, session: SessionLocal):
        self.session = session

    def create(self, appointment: Appointment):
        self.session.add(appointment)
        self.session.commit()

    def get_all(self):
        return self.session.query(Appointment).all()

    def get_by_id(self, id: int):
        return self.session.query(Appointment).filter(Appointment.id == id).first()

    def update(self, id: int, appointment: Appointment):
        existing_appointment = self.get_by_id(id)
        if existing_appointment:
            existing_appointment.name = appointment.name
            existing_appointment.date = appointment.date
            existing_appointment.time = appointment.time
            self.session.commit()
        else:
            raise ValueError("Appointment not found")

    def delete(self, id: int):
        appointment = self.get_by_id(id)
        if appointment:
            self.session.delete(appointment)
            self.session.commit()
        else:
            raise ValueError("Appointment not found")

# Create the database tables
Base.metadata.create_all(engine)

# Example usage
if __name__ == "__main__":
    # Create a new session
    session = SessionLocal()

    # Create a new repository
    repository = AppointmentRepository(session)

    # Create a new appointment
    appointment = Appointment(name="John Doe", date="2024-07-15", time="10:00")
    repository.create(appointment)

    # Get all appointments
    appointments = repository.get_all()
    for appointment in appointments:
        print(appointment)

    # Get an appointment by ID
    appointment = repository.get_by_id(1)
    print(appointment)

    # Update an appointment
    appointment = Appointment(name="Jane Doe", date="2024-07-16", time="11:00")
    repository.update(1, appointment)

    # Delete an appointment
    repository.delete(1)
```

This code follows the Clean Architecture principles and uses SQLAlchemy 2.0 for database operations. It defines a `Appointment` model and a `AppointmentRepository` interface for CRUD operations. The repository uses a `SessionLocal` object to interact with the database. The example usage demonstrates how to create a new appointment, get all appointments, get an appointment by ID, update an appointment, and delete an appointment.