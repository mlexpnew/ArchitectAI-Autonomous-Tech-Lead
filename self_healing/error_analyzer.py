"""
AI Error Analyzer
"""

from generators.ai.code_generator import AICodeGenerator


class ErrorAnalyzer:

    def __init__(self):

        self.ai = AICodeGenerator()

    def analyze(
        self,
        error: str,
        code: str,
    ) -> str:

        prompt = f"""
You are a Principal Software Engineer.

Analyze the following error.

Error:

{error}

Code:

{code}

Return ONLY:

1. Root Cause
2. Exact Fix

No markdown.
"""

        return self.ai.generate(prompt)