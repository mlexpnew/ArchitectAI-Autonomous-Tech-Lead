"""
AI Module Generator

Generates an entire entity module in one AI request.
"""

from pathlib import Path

from generators.ai.code_generator import AICodeGenerator
from generators.writer import FileWriter


class AIModuleGenerator:

    def __init__(self, output_dir: str):

        self.output_dir = Path(output_dir)

        self.ai = AICodeGenerator()

    def generate(
        self,
        entity_name: str,
        fields: list[str],
    ):
        print("Generating module for", entity_name)

        prompt = f"""
Generate a complete FastAPI module.

Entity:
{entity_name}

Fields:
{chr(10).join(fields)}

Return EXACTLY this format.

MODEL_START
...
MODEL_END

SCHEMA_START
...
SCHEMA_END

REPOSITORY_START
...
REPOSITORY_END

SERVICE_START
...
SERVICE_END

API_START
...
API_END

Return ONLY code.
"""

        response = self.ai.generate(prompt)

        self._save(entity_name, response)

    def _extract(
        self,
        text: str,
        start: str,
        end: str,
    ):

        if start not in text:
            return ""

        return (
            text.split(start)[1]
            .split(end)[0]
            .strip()
        )

    def _save(
        self,
        entity_name,
        text,
    ):

        entity = entity_name.lower()

        mapping = {

            "models": (
                "MODEL_START",
                "MODEL_END",
                f"{entity}.py",
            ),

            "schemas": (
                "SCHEMA_START",
                "SCHEMA_END",
                f"{entity}.py",
            ),

            "repositories": (
                "REPOSITORY_START",
                "REPOSITORY_END",
                f"{entity}_repository.py",
            ),

            "services": (
                "SERVICE_START",
                "SERVICE_END",
                f"{entity}_service.py",
            ),

            "api": (
                "API_START",
                "API_END",
                f"{entity}s.py",
            ),
        }

        for folder, values in mapping.items():

            start, end, filename = values

            code = self._extract(
                text,
                start,
                end,
            )

            if code:

                FileWriter.write(

                    self.output_dir
                    / "backend"
                    / "app"
                    / folder
                    / filename,

                    code,

                )

                print(f"✅ {folder}/{filename}")