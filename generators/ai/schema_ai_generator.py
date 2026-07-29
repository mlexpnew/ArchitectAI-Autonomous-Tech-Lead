"""
AI Schema Generator
"""

from pathlib import Path

from generators.ai.code_generator import AICodeGenerator
from generators.writer import FileWriter


class AISchemaGenerator:

    def __init__(self, output_dir: str):

        self.output_dir = Path(output_dir)

        self.ai = AICodeGenerator()

    def generate(
        self,
        entity_name: str,
        fields: list[str],
    ):

        prompt = f"""
Generate production-ready Pydantic V2 schemas.

Entity:

{entity_name}

Fields:

{chr(10).join(fields)}

Requirements:

- PatientCreate
- PatientUpdate
- PatientResponse

Rules:

- Pydantic V2
- Type hints
- from_attributes=True
- Output ONLY Python code
"""

        code = self.ai.generate(prompt)

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "schemas"
            / f"{entity_name.lower()}.py",
            code,
        )

        print(f"✅ Generated {entity_name} schema")