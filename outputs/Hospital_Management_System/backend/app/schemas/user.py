from pydantic import BaseModel
from .models.user import User

class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    role: str

    class Config:
        orm_mode = True