"""
Infrastructure Generator
"""

from pathlib import Path

from generators.writer import FileWriter


class InfrastructureGenerator:

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def generate_requirements(self):

        requirements = """fastapi
uvicorn[standard]
sqlalchemy
pydantic
python-dotenv
alembic
"""

        FileWriter.write(
            self.output_dir / "backend" / "requirements.txt",
            requirements,
        )

        print("✅ requirements.txt")

    def generate_env(self):

        env = """DATABASE_URL=sqlite:///./app.db
SECRET_KEY=CHANGE_ME
API_VERSION=v1
"""

        FileWriter.write(
            self.output_dir / "backend" / ".env.example",
            env,
        )

        print("✅ .env.example")

    def generate(self):

        self.generate_requirements()

        self.generate_env()