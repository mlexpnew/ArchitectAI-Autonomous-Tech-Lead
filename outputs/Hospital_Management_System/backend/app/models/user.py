from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    role = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"

class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    role: str

    class Config:
        orm_mode = True