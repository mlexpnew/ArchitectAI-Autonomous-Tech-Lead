"""
Autonomous Tech Lead
"""

import json


from generators.ai.code_generator import AICodeGenerator
from techlead.decision import Decision


class TechLead:

    def __init__(self):
        self.ai = AICodeGenerator()

    def evaluate(self, state):

        prompt = f"""
You are an Engineering Director.

Project:
{state.project_name}

Completed:
{state.completed}

Failed:
{state.failed}

Return ONLY valid JSON.

Example:

{{
    "continue_project": true,
    "retry_agents": [],
    "new_tasks": [],
    "message": "Project is progressing normally."
}}
"""

        result = self.ai.generate(prompt)

        print("\n========== RAW TECH LEAD RESPONSE ==========\n")
        print(result)
        print("\n============================================\n")

        result = (
            result.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        start = result.find("{")

        if start == -1:
            raise ValueError("No JSON returned.")

        depth = 0
        end = None

        for i in range(start, len(result)):
            if result[i] == "{":
                depth += 1
            elif result[i] == "}":
                depth -= 1

                if depth == 0:
                    end = i + 1
                    break

        if end is None:
            raise ValueError("Invalid JSON.")

        json_text = result[start:end]

        data = json.loads(json_text)

        return Decision(**data)