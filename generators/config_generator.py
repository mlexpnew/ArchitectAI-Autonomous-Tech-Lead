"""
Configuration Generator

Generates environment and application configuration
for dynamically generated backend projects.
"""

from pathlib import Path

from generators.writer import FileWriter


class ConfigGenerator:

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def generate(self):

        # -------------------------------------------------
        # Generate .env.example
        # -------------------------------------------------

        env_example = """APP_NAME=Generated API
APP_ENV=development
DEBUG=true

DATABASE_URL=sqlite:///./app.db

HOST=127.0.0.1
PORT=8000
"""

        FileWriter.write(
            self.output_dir
            / "backend"
            / ".env.example",
            env_example,
        )

        # -------------------------------------------------
        # Generate config.py
        # -------------------------------------------------

        config_code = '''"""
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
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "config.py",
            config_code,
        )

        print("✅ Generated environment configuration")