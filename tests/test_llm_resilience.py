"""
Unit tests for LLM provider resilience, multi-provider dispatch,
safe initialization, and mock execution mode.
"""

import pytest

from config.settings import Settings
from config.llm import _init_llm
from generators.ai.code_generator import AICodeGenerator


def test_settings_provider_fallback_to_gemini():
    """Verify that if Groq key is missing but Google key is present, provider resolves to gemini."""
    s = Settings(
        LLM_PROVIDER="groq",
        GROQ_API_KEY="",
        GOOGLE_API_KEY="test_gemini_key",
    )
    assert s.get_active_provider() == "gemini"
    assert s.has_valid_api_key() is True
    assert s.get_active_model() == s.GEMINI_MODEL


def test_settings_provider_fallback_to_openai():
    """Verify fallback to OpenAI when Groq and Gemini keys are missing."""
    s = Settings(
        LLM_PROVIDER="groq",
        GROQ_API_KEY="",
        GOOGLE_API_KEY="",
        OPENAI_API_KEY="sk-test",
    )
    assert s.get_active_provider() == "openai"
    assert s.has_valid_api_key() is True
    assert s.get_active_model() == s.OPENAI_MODEL


def test_settings_ollama_provider():
    """Verify Ollama local provider resolution."""
    s = Settings(
        LLM_PROVIDER="ollama",
    )
    assert s.get_active_provider() == "ollama"
    assert s.has_valid_api_key() is True
    assert s.get_active_model() == s.OLLAMA_MODEL


def test_settings_mock_mode():
    """Verify MOCK_LLM mode flag."""
    s = Settings(
        MOCK_LLM=True,
    )
    assert s.get_active_provider() == "mock"
    assert s.has_valid_api_key() is True


def test_ai_code_generator_safe_init_without_key(monkeypatch):
    """Ensure AICodeGenerator does not crash at initialization time when API key is missing."""
    monkeypatch.setattr("generators.ai.code_generator.settings.GROQ_API_KEY", None)
    monkeypatch.setattr("config.settings.settings.GROQ_API_KEY", None)
    gen = AICodeGenerator(provider="groq", mock_mode=False)
    assert gen.client is None
    assert gen.provider == "groq"


def test_ai_code_generator_raises_explicit_error_without_key(monkeypatch):
    """Ensure calling generate() without credentials raises an informative RuntimeError."""
    monkeypatch.setattr("generators.ai.code_generator.settings.GROQ_API_KEY", None)
    monkeypatch.setattr("config.settings.settings.GROQ_API_KEY", None)
    gen = AICodeGenerator(provider="groq", mock_mode=False)
    with pytest.raises(RuntimeError) as exc_info:
        gen.generate("Create a model")
    assert "No API key configured for provider 'groq'" in str(exc_info.value)
    assert "GROQ_API_KEY" in str(exc_info.value)


def test_ai_code_generator_mock_mode_code():
    """Ensure mock mode returns valid mock code without making any network calls."""
    gen = AICodeGenerator(mock_mode=True)
    output = gen.generate("Create a service class")
    assert "Mock" in output
    assert "class" in output


def test_ai_code_generator_mock_mode_json():
    """Ensure mock mode returns valid JSON array when requested in prompt."""
    import json
    gen = AICodeGenerator(mock_mode=True)
    output = gen.generate("Extract entities in JSON format")
    data = json.loads(output)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "entity" in data[0]


def test_crewai_llm_init():
    """Ensure CrewAI LLM initializes without raising ImportError."""
    crew_llm = _init_llm()
    assert crew_llm is not None
    assert hasattr(crew_llm, "model")
