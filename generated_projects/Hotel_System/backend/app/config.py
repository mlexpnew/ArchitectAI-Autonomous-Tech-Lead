"""
Application Configuration
"""

import os


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "Generated API",
    )

    APP_ENV = os.getenv(
        "APP_ENV",
        "development",
    )

    DEBUG = os.getenv(
        "DEBUG",
        "true",
    ).lower() == "true"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db",
    )

    HOST = os.getenv(
        "HOST",
        "127.0.0.1",
    )

    PORT = int(
        os.getenv(
            "PORT",
            "8000",
        )
    )


settings = Settings()
