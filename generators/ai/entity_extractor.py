"""
AI Entity Extractor

Extracts entities from project requirements.
"""

import json
from urllib import response

from generators import entities
from generators.ai.code_generator import AICodeGenerator
from generators.entities import entity
from utils.json_parser import JSONParser
from generators.entities.entity import Entity
from generators.entities.entity import EntityField


class AIEntityExtractor:

    def __init__(self):

        self.ai = AICodeGenerator()

    def extract(
        self,
        requirements: str,
    ):

        prompt = f"""
You are a Senior Software Architect.

Read the software requirements.

Extract all database entities.

Return ONLY valid JSON.

Format:

[
    {{
        "entity":"Patient",
        "fields":[
            "id : integer",
            "name : string",
            "age : integer"
        ]
    }}
]

Requirements:

{requirements}
"""

        response = self.ai.generate(
            prompt,
            system_prompt="""
        You are a Senior Software Architect.

        Extract database entities from software requirements.

        Return ONLY valid JSON.

        Do NOT generate Python code.
        Do NOT generate SQLAlchemy models.
        Do NOT generate FastAPI code.
        Do NOT generate explanations.
        Do NOT generate markdown.

        Return exactly this format:

        [
            {
                "entity": "Patient",
                "fields": [
                    "id : integer",
                    "name : string",
                    "age : integer"
                ]
            }
        ]
        """
        )

        print("\n========== RAW ENTITY AI RESPONSE ==========\n")
        print(response)
        print("\n===========================================\n")

        data = JSONParser.parse(response)

        entities = []

        for item in data:

            entity = Entity(
                name=item["entity"]
            )

            for field in item["fields"]:
                if isinstance(field, dict):
                    name = field.get("name") or field.get("field") or list(field.keys())[0]
                    datatype = field.get("type") or field.get("datatype") or list(field.values())[0]
                elif isinstance(field, str):
                    if ":" in field:
                        name, datatype = field.split(":", 1)
                    else:
                        name, datatype = field, "string"
                else:
                    name, datatype = str(field), "string"

                entity.fields.append(
                    EntityField(
                        name=str(name).strip(),
                        type=str(datatype).strip()
                    )
                )

            entities.append(entity)

        return entities

        