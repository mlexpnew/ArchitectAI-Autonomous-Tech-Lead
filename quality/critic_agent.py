"""
AI Critic Agent
"""

from generators.ai.code_generator import AICodeGenerator


class CriticAgent:

    def __init__(self):

        self.ai = AICodeGenerator()

    def review(
        self,
        code: str,
    ):

        prompt = f"""
You are a Principal Software Architect.

Review the following code.

Score the code from 0-100.

Evaluate:

- SOLID
- Clean Architecture
- FastAPI
- SQLAlchemy
- Python 3.12
- Security
- Performance
- Readability
- Maintainability

Return ONLY valid JSON.

Example:

{{
    "score":92,
    "approved":true,
    "issues":[
        "Repository should use dependency injection."
    ]
}}

Code:

{code}
"""

        response = self.ai.generate(prompt)

        response = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        import json

        return json.loads(response)