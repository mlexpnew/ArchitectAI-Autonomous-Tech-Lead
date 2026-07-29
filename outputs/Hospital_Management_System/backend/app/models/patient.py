models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Patient(id={self.id}, name='{self.name}', age={self.age}, phone='{self.phone}')"


__init__.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


main.py

from fastapi import FastAPI
from . import __init__

app = FastAPI()

SQLALCHEMY_DATABASE_URL = __init__.SQLALCHEMY_DATABASE_URL

@app.on_event("shutdown")
def shutdown_event():
    SessionLocal().close()