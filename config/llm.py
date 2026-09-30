"""
LLM Configuration
"""

from crewai import LLM
from config.settings import settings


def _init_llm() -> LLM:
    """
    Initializes CrewAI LLM with multi-provider support.
    Uses OpenAI-compatible endpoints to support Groq, Gemini, and Ollama
    without requiring optional external packages like LiteLLM.
    """
    provider = settings.get_active_provider()

    if provider == "groq":
        return LLM(
            model=f"openai/{settings.MODEL_NAME}",
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY or "gsk_placeholder",
            temperature=settings.MODEL_TEMPERATURE,
        )

    if provider in ("google", "gemini"):
        return LLM(
            model=f"openai/{settings.GEMINI_MODEL}",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=settings.GOOGLE_API_KEY or "gemini_placeholder",
            temperature=settings.MODEL_TEMPERATURE,
        )

    if provider == "openai":
        return LLM(
            model=f"openai/{settings.OPENAI_MODEL}",
            api_key=settings.OPENAI_API_KEY or "sk_placeholder",
            temperature=settings.MODEL_TEMPERATURE,
        )

    if provider == "ollama":
        return LLM(
            model=f"openai/{settings.OLLAMA_MODEL}",
            base_url=settings.OLLAMA_BASE_URL,
            api_key="ollama",
            temperature=settings.MODEL_TEMPERATURE,
        )

    return LLM(
        model=settings.get_active_model(),
        temperature=settings.MODEL_TEMPERATURE,
    )


llm = _init_llm()