"""
AI Code Generator

Uses Groq to generate production-ready code.
"""

import time

from groq import Groq, RateLimitError

from config.settings import settings
from quality.prompt_optimizer import PromptOptimizer


class AICodeGenerator:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.MODEL_NAME

        self.optimizer = PromptOptimizer()

    def generate(
    self,
    prompt: str,
    project_context: str = "",
    system_prompt: str | None = None,
) -> str:

        # Optimize prompt
        prompt = self.optimizer.optimize(
            prompt,
            code_generation=(system_prompt is None),
        )

        while True:
            try:
                default_system_prompt = (
                    "You are a Principal Software Architect.\n"
                    "Generate production-ready code.\n"
                    "Return ONLY code.\n"
                    "Never return markdown.\n"
                    "Never return explanations.\n"
                    "Never wrap code inside ``` blocks."
                )

                messages = [
                    {
                        "role": "system",
                        "content": system_prompt or default_system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=settings.MODEL_TEMPERATURE,
                )

                result = response.choices[0].message.content.strip()

                # ----------------------------------------
                # Cleanup AI Output
                # ----------------------------------------

                result = (
                    result.replace("```python", "")
                    .replace("```", "")
                    .strip()
                )

                remove_after = [
                    "However,",
                    "Explanation",
                    "Notes:",
                    "Note:",
                    "Here is",
                    "This code",
                    "The above",
                    "Hope this helps",
                ]

                for marker in remove_after:
                    if marker in result:
                        result = result.split(marker)[0].strip()

                return result

            except RateLimitError:
                print("⏳ Groq rate limit reached. Waiting 2 seconds...")
                time.sleep(2)

            except Exception as e:
                print(f"❌ AI Generation Error: {e}")
                raise