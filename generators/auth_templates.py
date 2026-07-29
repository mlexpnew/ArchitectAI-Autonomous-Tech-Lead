"""
Authentication Templates
"""


def password_template():

    return '''"""
Password Utilities
"""

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
):

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )
'''


def jwt_template():

    return '''"""
JWT Utilities
"""

from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "CHANGE_ME"

ALGORITHM = "HS256"


def create_access_token(data: dict):

    payload = data.copy()

    payload["exp"] = datetime.utcnow() + timedelta(hours=24)

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
'''