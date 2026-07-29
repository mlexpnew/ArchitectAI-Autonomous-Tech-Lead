"""
Database Generator
"""

from pathlib import Path

from generators.writer import FileWriter

class DatabaseGenerator:

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)

    def generate(self):

        code = '''"""
Database Configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False}
        if DATABASE_URL.startswith("sqlite")
        else {}
    ),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "database.py",
            code,
        )

        print("✅ Generated database.py")