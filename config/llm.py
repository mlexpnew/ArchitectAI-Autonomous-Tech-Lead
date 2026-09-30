"""
LLM Configuration & Multi-Model Router
"""

from typing import Any
from crewai import LLM
from config.settings import settings


def get_available_router_models() -> list[dict[str, Any]]:
    """
    Catalog of models available for real-time switching in the router.
    """
    return [
        {
            "id": "claude-3-5-sonnet-20241022",
            "name": "Claude 3.5 Sonnet",
            "provider": "anthropic",
            "description": "Anthropic flagship · SOTA coding reasoning & architectural planning",
            "badge": "🟣 Flagship Reasoning",
            "input_cost": "$3.00 / 1M",
            "output_cost": "$15.00 / 1M",
        },
        {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "provider": "openai",
            "description": "OpenAI flagship · High-speed multimodal intelligence",
            "badge": "🟢 Flagship Multimodal",
            "input_cost": "$2.50 / 1M",
            "output_cost": "$10.00 / 1M",
        },
        {
            "id": "gemini-2.5-flash",
            "name": "Gemini 2.5 Flash",
            "provider": "gemini",
            "description": "Google ultra-fast · 1M token context & 97%+ cost reduction",
            "badge": "⚡ Cost-Optimized",
            "input_cost": "$0.075 / 1M",
            "output_cost": "$0.30 / 1M",
        },
        {
            "id": "ollama",
            "name": "Ollama Local (Llama 3.2)",
            "provider": "ollama",
            "description": "100% On-Premise · Air-gapped & $0.00 zero cloud spend",
            "badge": "🦙 Air-Gapped / Free",
            "input_cost": "$0.00 (Local)",
            "output_cost": "$0.00 (Local)",
        },
        {
            "id": "qwen/qwen3.8-27b",
            "name": "Groq Qwen 3.8",
            "provider": "groq",
            "description": "Groq LPU hardware · Instantaneous inference velocity",
            "badge": "🚀 Ultra-Low Latency",
            "input_cost": "$0.59 / 1M",
            "output_cost": "$0.79 / 1M",
        },
    ]


def _init_llm(provider_override: str | None = None, model_override: str | None = None) -> LLM:
    """
    Initializes CrewAI LLM with multi-provider support.
    Supports Anthropic Claude 3.5, OpenAI GPT-4o, Google Gemini Flash,
    Ollama Local, and Groq LPU.
    """
    provider = provider_override or settings.get_active_provider()

    if provider == "mock" or settings.MOCK_LLM:
        return LLM(
            model="openai/gpt-4o-mini",
            api_key="mock_key",
            temperature=settings.MODEL_TEMPERATURE,
        )

    if provider == "groq":
        model_name = model_override or settings.MODEL_NAME
        return LLM(
            model=f"openai/{model_name}",
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY or "gsk_placeholder",
            temperature=settings.MODEL_TEMPERATURE,
        )

    if provider in ("google", "gemini"):
        model_name = model_override or settings.GEMINI_MODEL
        return LLM(
            model=f"openai/{model_name}",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=settings.GOOGLE_API_KEY or "gemini_placeholder",
            temperature=settings.MODEL_TEMPERATURE,
        )

    if provider == "openai":
        model_name = model_override or settings.OPENAI_MODEL
        return LLM(
            model=f"openai/{model_name}",
            api_key=settings.OPENAI_API_KEY or "sk_placeholder",
            temperature=settings.MODEL_TEMPERATURE,
        )

    if provider == "anthropic":
        model_name = model_override or settings.ANTHROPIC_MODEL
        return LLM(
            model=f"anthropic/{model_name}",
            api_key=settings.ANTHROPIC_API_KEY or "anthropic_placeholder",
            temperature=settings.MODEL_TEMPERATURE,
        )

    if provider == "ollama":
        model_name = model_override or settings.OLLAMA_MODEL
        return LLM(
            model=f"openai/{model_name}",
            base_url=settings.OLLAMA_BASE_URL,
            api_key="ollama",
            temperature=settings.MODEL_TEMPERATURE,
        )

    active_model = settings.get_active_model()
    if "/" not in active_model or not any(active_model.startswith(p + "/") for p in ("openai", "anthropic", "azure", "gemini", "google", "ollama")):
        active_model = f"openai/{active_model}"

    return LLM(
        model=active_model,
        temperature=settings.MODEL_TEMPERATURE,
    )


llm = _init_llm()


def get_llm(model_key: str | None = None) -> LLM:
    """
    Factory to retrieve configured LLM, dynamically adjusting to active router model.
    """
    if not model_key:
        return _init_llm()

    settings.switch_model(model_key)
    return _init_llm()