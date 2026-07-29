"""
Backend Generator
"""

from generators.ai.code_generator import AICodeGenerator


class BackendGenerator:

    def __init__(self):

        self.ai = AICodeGenerator()

    def generate_service(self, entity):

        prompt = f"""
Generate a production-ready FastAPI service.

Requirements:

- Entity: {entity}
- CRUD APIs
- Type Hints
- Clean Code
- Python Only

Return ONLY Python code.
"""

        return self.ai.generate(prompt)