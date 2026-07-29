"""
Prompt Optimizer
"""


class PromptOptimizer:

    def optimize(
        self,
        prompt: str,
        code_generation: bool = True,
    ):

        if not code_generation:
            return prompt

        rules = """
Rules

Return ONLY Python code.

No markdown.

No explanation.

No comments outside code.

No ```python

No Example section.

No Notes.

No However.

Generate production-ready code.

Python 3.12

SQLAlchemy 2.0

FastAPI Best Practices.
"""

        return rules + "\n\n" + prompt