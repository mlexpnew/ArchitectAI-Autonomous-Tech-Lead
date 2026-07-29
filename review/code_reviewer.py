"""
AI Code Reviewer
"""

from pathlib import Path

from generators.ai.code_generator import AICodeGenerator


class CodeReviewer:

    def __init__(self):

        self.ai = AICodeGenerator()

        self.prompt = Path(
            "review/review_prompt.md"
        ).read_text(
            encoding="utf-8"
        )

    def review(
        self,
        code: str,
    ) -> str:

        prompt = self.prompt.replace(
            "{code}",
            code,
        )

        return self.ai.generate(prompt)