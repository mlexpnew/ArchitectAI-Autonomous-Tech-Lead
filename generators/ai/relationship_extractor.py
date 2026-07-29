"""
AI Relationship Extractor

Extracts relationships between entities from project requirements.
"""

from generators.ai.code_generator import AICodeGenerator
from generators.entities.relationship import Relationship
from utils.json_parser import JSONParser


class RelationshipExtractor:

    def __init__(self):
        self.ai = AICodeGenerator()

    def extract(
        self,
        requirements: str,
    ):

        prompt = f"""
You are a Senior Software Architect.

Analyze the following software requirements.

Extract relationships between database entities.

Return ONLY valid JSON.

IMPORTANT:

Return ONE JSON object containing a
"relationships" array.

Required format:

{{
    "relationships": [
        {{
            "source": "Patient",
            "target": "Appointment",
            "relationship_type": "one_to_many",
            "foreign_key": "patient_id"
        }}
    ]
}}

Allowed relationship types:

- one_to_one
- one_to_many
- many_to_one
- many_to_many

Rules:

1. Return valid JSON only.
2. Do not return markdown.
3. Do not return explanations.
4. Do not return multiple top-level JSON objects.
5. Do not duplicate inverse relationships.
6. foreign_key may be null for many-to-many relationships.

Requirements:

{requirements}
"""

        response = self.ai.generate(
            prompt,
            system_prompt="""
You are a Senior Software Architect.

Extract ONLY entity relationships.

Return ONLY valid JSON.

Do NOT generate Python code.
Do NOT generate SQLAlchemy models.
Do NOT generate FastAPI code.
Do NOT generate explanations.
Do NOT generate markdown.

Return exactly:

{
    "relationships": [
        {
            "source": "Patient",
            "target": "Appointment",
            "relationship_type": "one_to_many",
            "foreign_key": "patient_id"
        }
    ]
}
"""
        )

        print("\n========== RAW AI RESPONSE ==========\n")
        print(response)
        print("\n=====================================\n")

        # --------------------------------------------------
        # Robust JSON Parsing
        # --------------------------------------------------

        data = JSONParser.parse(response)

        # JSONParser may return:
        # 1. {"relationships":[...]}
        # 2. [...]
        # 3. {...}

        if isinstance(data, dict):

            if "relationships" in data:
                data = data["relationships"]

            elif (
                "source" in data
                and "target" in data
                and "relationship_type" in data
            ):
                data = [data]

            else:
                raise ValueError(
                    "Unexpected relationship JSON structure."
                )

        if not isinstance(data, list):
            raise ValueError(
                "Relationship response must contain a list."
            )

        print(type(data))
        print(data)

        relationships = []

        for item in data:

            if not isinstance(item, dict):
                continue

            source = item.get("source")
            target = item.get("target")
            relationship_type = item.get("relationship_type")
            foreign_key = item.get("foreign_key")

            if not source or not target or not relationship_type:
                continue

            relationships.append(
                Relationship(
                    source=source,
                    target=target,
                    relationship_type=relationship_type,
                    foreign_key=foreign_key,
                )
            )

        return relationships