"""
AI API Generator

Generates FastAPI CRUD APIs using AI.
"""

from pathlib import Path

from generators.ai.code_generator import AICodeGenerator
from generators.writer import FileWriter


class AIAPIGenerator:

    def __init__(self, output_dir: str):

        self.output_dir = Path(output_dir)

        self.ai = AICodeGenerator()

    def generate(
        self,
        entity_name: str,
    ):

        prompt = f"""
Generate a production-ready FastAPI CRUD Router.

Entity:

{entity_name}

Requirements:

- FastAPI
- SQLAlchemy Session Dependency
- Pydantic V2
- CRUD Endpoints

Required Endpoints:

GET /
GET /{{id}}
POST /
PUT /{{id}}
DELETE /{{id}}

Use:

Repository Layer

Service Layer

Dependency Injection

Python 3.12

Return ONLY Python code.
"""

        code = self.ai.generate(prompt)

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "api"
            / f"{entity_name.lower()}s.py",
            code,
        )

        print(f"✅ Generated {entity_name} API")