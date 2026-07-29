"""
AI Reviewer
"""

import re

from generators.ai.code_generator import AICodeGenerator

from reviewer.review import Review


class ReviewerAgent:

    def __init__(self):

        self.ai = AICodeGenerator()

    def review(self, code: str):

        prompt = f"""
You are a Senior Software Engineer.

Review the following Python code.

Return ONLY JSON.

Example:

{{
    "passed": true,
    "score": 92,
    "feedback": "Looks good."
}}

Code:

{code}
"""

        result = self.ai.generate(prompt)

        result = (
            result
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        match = re.search(r"\{[\s\S]*\}", result)

        if not match:
            return Review(
                False,
                0,
                "Reviewer returned invalid JSON."
            )

        import json

        data = json.loads(match.group())

        return Review(**data)