"""
AI Code Fixer
"""

from generators.ai.code_generator import AICodeGenerator


class CodeFixer:

    def __init__(self):

        self.ai = AICodeGenerator()

    def fix(
        self,
        code: str,
        error: str,
    ) -> str:

        prompt = f"""
You are a Senior Python Engineer.

The following Python code contains syntax errors.

Return ONLY corrected Python code.

Rules:

- No markdown
- No explanation
- No comments
- No ```python
- Return a complete file
- Ensure the code compiles with Python 3.12
- Return ONLY valid Python code.
- Do NOT add explanations.
- Do NOT wrap the code inside ```python blocks.
- Do NOT use markdown.

Syntax Error:

{error}

Python Code:

{code}
"""

        fixed = self.ai.generate(prompt)

        # Remove markdown if the model still returns it
        fixed = (
            fixed.replace("```python", "")
                 .replace("```", "")
                 .strip()
        )

        print("\n" + "=" * 80)
        print("FIXED CODE")
        print("=" * 80)
        print(fixed)
        print("=" * 80)

        return fixed