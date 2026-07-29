"""
Application Configuration
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "ArchitectAI"

    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost/hospital_db"
    )

    SECRET_KEY: str = "CHANGE_ME"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
