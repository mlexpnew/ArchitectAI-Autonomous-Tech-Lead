"""
LLM Configuration
"""

from crewai import LLM
from config.settings import settings


def _init_llm() -> LLM:
    """
    Initializes CrewAI LLM.
    Uses OpenAI-compatible endpoint for Groq to support environments
    where LiteLLM is not installed.
    """
    provider = getattr(settings, "LLM_PROVIDER", "groq").lower()

    if provider == "groq":
        return LLM(
            model=f"openai/{settings.MODEL_NAME}",
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY or "gsk_placeholder",
            temperature=settings.MODEL_TEMPERATURE,
        )

    return LLM(
        model=settings.MODEL_NAME,
        temperature=settings.MODEL_TEMPERATURE,
    )


llm = _init_llm()