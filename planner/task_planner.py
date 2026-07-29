"""
AI Project Planner
"""

import json
import re

from generators.ai.code_generator import AICodeGenerator
from planner.task import ProjectTask


class TaskPlanner:

    def __init__(self):

        self.ai = AICodeGenerator()

    def _extract_json(self, text: str):

        # Remove markdown
        text = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # Find first JSON array
        match = re.search(r"\[[\s\S]*\]", text)

        if not match:
            raise ValueError(
                "Planner did not return valid JSON."
            )

        return match.group(0)

    def plan(
        self,
        project: str,
    ):

        prompt = f"""
You are a Senior Software Architect.

Project:

{project}

Create a task list.

Return ONLY a JSON array.

Example:

[
  {{
    "agent":"database",
    "title":"Generate Models",
    "description":"Create SQLAlchemy Models",
    "depends_on":[]
  }},
  {{
    "agent":"backend",
    "title":"Generate APIs",
    "description":"Generate FastAPI APIs",
    "depends_on":["database"]
  }},
  {{
    "agent":"security",
    "title":"Security Scan",
    "description":"Review backend security",
    "depends_on":["backend"]
  }},
  {{
    "agent":"qa",
    "title":"Generate Tests",
    "description":"Generate pytest",
    "depends_on":["backend"]
  }},
  {{
    "agent":"documentation",
    "title":"Generate README",
    "description":"Write documentation",
    "depends_on":["backend","qa"]
  }}
]
"""

        result = self.ai.generate(
            prompt=prompt,
        )

        print("\n========== RAW AI RESPONSE ==========\n")
        print(result)
        print("\n=====================================\n")

        json_text = self._extract_json(result)

        tasks = json.loads(json_text)

        return [
            ProjectTask(**task)
            for task in tasks
        ]