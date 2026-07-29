```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///schedule.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f"Schedule(id={self.id}, name='{self.name}', description='{self.description}')"

Base.metadata.create_all(engine)

class ScheduleRepository:
    def __init__(self, session: SessionLocal):
        self.session = session

    def create(self, schedule: Schedule):
        self.session.add(schedule)
        self.session.commit()
        return schedule

    def get_all(self):
        return self.session.query(Schedule).all()

    def get_by_id(self, id: int):
        return self.session.query(Schedule).filter(Schedule.id == id).first()

    def update(self, id: int, schedule: Schedule):
        existing_schedule = self.get_by_id(id)
        if existing_schedule:
            existing_schedule.name = schedule.name
            existing_schedule.description = schedule.description
            self.session.commit()
            return existing_schedule
        return None

    def delete(self, id: int):
        schedule = self.get_by_id(id)
        if schedule:
            self.session.delete(schedule)
            self.session.commit()
            return True
        return False

class ScheduleSchema(BaseModel):
    id: int
    name: str
    description: str

class ScheduleService:
    def __init__(self, repository: ScheduleRepository):
        self.repository = repository

    def create_schedule(self, schedule: ScheduleSchema):
        return self.repository.create(Schedule(**schedule.dict()))

    def get_all_schedules(self):
        return self.repository.get_all()

    def get_schedule_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def update_schedule(self, id: int, schedule: ScheduleSchema):
        return self.repository.update(id, Schedule(**schedule.dict()))

    def delete_schedule(self, id: int):
        return self.repository.delete(id)
```

This code adheres to the Clean Architecture principles and provides a production-ready SQLAlchemy repository for the Schedule entity. It includes CRUD operations and uses Pydantic for schema validation. The code is written in Python 3.12 and uses SQLAlchemy 2.0.