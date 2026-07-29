"""
AI Service Generator
"""

from pathlib import Path

from generators.ai.code_generator import AICodeGenerator
from generators.writer import FileWriter


class AIServiceGenerator:

    def __init__(self, output_dir: str):

        self.output_dir = Path(output_dir)

        self.ai = AICodeGenerator()

    def generate(
        self,
        entity_name: str,
    ):

        prompt = f"""
Generate a production-ready Service Layer.

Entity:

{entity_name}

Requirements:

- Business Logic
- CRUD
- Validation
- Repository Pattern

Rules:

- Python 3.12
- Output ONLY Python code
"""

        code = self.ai.generate(prompt)

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "services"
            / f"{entity_name.lower()}_service.py",
            code,
        )

        print(f"✅ Generated {entity_name} Service")