"""
Requirements Generator

Generates dependency files for generated backend projects.
"""

from pathlib import Path

from generators.writer import FileWriter


class RequirementsGenerator:

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def generate(self):

        requirements = """fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
pytest>=8.0.0
httpx>=0.27.0
"""

        FileWriter.write(
            self.output_dir
            / "backend"
            / "requirements.txt",
            requirements,
        )

        print("✅ Generated requirements.txt")