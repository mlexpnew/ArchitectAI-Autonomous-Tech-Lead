"""
AI Repository Generator
"""

from pathlib import Path

from generators.ai.code_generator import AICodeGenerator
from generators.writer import FileWriter


class AIRepositoryGenerator:

    def __init__(self, output_dir: str):

        self.output_dir = Path(output_dir)

        self.ai = AICodeGenerator()

    def generate(
        self,
        entity_name: str,
    ):

        prompt = f"""
Generate a production-ready SQLAlchemy Repository.

Entity:

{entity_name}

Requirements:

- SQLAlchemy 2.0
- CRUD operations
- create()
- get_all()
- get_by_id()
- update()
- delete()

Rules:

- Clean Architecture
- Python 3.12
- Output ONLY Python code
"""

        code = self.ai.generate(prompt)

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "repositories"
            / f"{entity_name.lower()}_repository.py",
            code,
        )

        print(f"✅ Generated {entity_name} Repository")