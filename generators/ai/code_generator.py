"""
AI Code Generator

Multi-provider code generation engine supporting Groq, Gemini, OpenAI,
Ollama, and offline Mock mode with resilient error handling.
"""

import json
import logging
import re
import time

from openai import OpenAI

from config.settings import settings
from quality.prompt_optimizer import PromptOptimizer

logger = logging.getLogger(__name__)


class AICodeGenerator:
    """
    Production-grade AI code generator with multi-provider abstraction.
    Supports Groq, Google Gemini, OpenAI, Ollama, and offline mock modes.
    """

    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
        mock_mode: bool | None = None,
    ):
        self.provider = (provider or settings.get_active_provider()).lower().strip()
        self.model = model or settings.get_active_model()
        self.mock_mode = settings.MOCK_LLM if mock_mode is None else mock_mode
        self.optimizer = PromptOptimizer()
        self.client = self._init_client()

    def _init_client(self) -> OpenAI | None:
        """
        Safely initializes the client for the configured provider.
        Does not crash if credentials are absent at startup.
        """
        if self.mock_mode or self.provider == "mock":
            return None

        if self.provider == "groq":
            api_key = settings.GROQ_API_KEY.strip()
            if not api_key:
                return None
            return OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1",
                timeout=settings.REQUEST_TIMEOUT,
            )

        if self.provider in ("google", "gemini"):
            api_key = settings.GOOGLE_API_KEY.strip()
            if not api_key:
                return None
            return OpenAI(
                api_key=api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                timeout=settings.REQUEST_TIMEOUT,
            )

        if self.provider == "openai":
            api_key = settings.OPENAI_API_KEY.strip()
            if not api_key:
                return None
            return OpenAI(
                api_key=api_key,
                timeout=settings.REQUEST_TIMEOUT,
            )

        if self.provider == "ollama":
            return OpenAI(
                api_key="ollama",
                base_url=settings.OLLAMA_BASE_URL,
                timeout=settings.REQUEST_TIMEOUT,
            )

        return None

    def _generate_mock_response(self, prompt: str) -> str:
        """
        Generates deterministic synthetic responses for offline testing.
        """
        # If prompt expects a JSON list (e.g. entity extractor or task planner)
        if "JSON" in prompt.upper() or "JSON ARRAY" in prompt.upper():
            if "TASK" in prompt.upper() or "AGENT" in prompt.upper():
                return json.dumps([
                    {
                        "agent": "database",
                        "title": "Generate Database Models",
                        "description": "Generate SQLAlchemy models for the schema",
                        "depends_on": [],
                    },
                    {
                        "agent": "backend",
                        "title": "Generate API Endpoints",
                        "description": "Generate FastAPI routers and business services",
                        "depends_on": ["database"],
                    },
                ])
            return json.dumps([
                {"entity": "User", "fields": [{"name": "id", "type": "int"}, {"name": "email", "type": "str"}]},
                {"entity": "Order", "fields": [{"name": "id", "type": "int"}, {"name": "user_id", "type": "int"}]},
            ])

        # Default mock code response
        return "# Mock generated module\nclass MockService:\n    pass\n"

    def generate(
        self,
        prompt: str,
        project_context: str = "",
        system_prompt: str | None = None,
    ) -> str:
        """
        Generates production-ready code with automatic retries and cleanup.
        """
        if self.mock_mode or self.provider == "mock":
            return self._generate_mock_response(prompt)

        # Check for client availability
        if self.client is None:
            key_map = {
                "groq": "GROQ_API_KEY",
                "gemini": "GOOGLE_API_KEY",
                "openai": "OPENAI_API_KEY",
            }
            key_name = key_map.get(self.provider, "API_KEY")
            raise RuntimeError(
                f"No API key configured for provider '{self.provider}'. "
                f"Please set {key_name} in your .env file or environment, "
                "or enable MOCK_LLM=True for offline execution."
            )

        # Optimize prompt
        prompt = self.optimizer.optimize(
            prompt,
            code_generation=(system_prompt is None),
        )

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

        max_retries = max(1, settings.MAX_RETRIES)
        last_error = None

        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=settings.MODEL_TEMPERATURE,
                )

                content = response.choices[0].message.content or ""
                result = content.strip()

                # ----------------------------------------
                # Cleanup AI Output
                # ----------------------------------------
                result = (
                    result.replace("```python", "")
                    .replace("```json", "")
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

            except Exception as exc:
                last_error = exc
                err_str = str(exc).lower()

                # Rate limiting or server congestion
                if "rate limit" in err_str or "429" in err_str:
                    wait_time = min(30, 2 ** attempt)
                    logger.warning(
                        f"Rate limit encountered on {self.provider} (attempt {attempt}/{max_retries}). "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                    continue

                logger.error(f"AI Generation Error on provider '{self.provider}': {exc}")
                raise

        raise RuntimeError(
            f"Failed to generate code after {max_retries} attempts: {last_error}"
        )