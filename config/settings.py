"""
Project Configuration

ArchitectAI - Autonomous Tech Lead

Centralized application configuration using Pydantic Settings.
Supports multiple LLM providers (Groq, Gemini, OpenAI, Ollama).
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ensure required storage directories exist
for _dir in ["outputs", "logs", "data"]:
    Path(_dir).mkdir(parents=True, exist_ok=True)

# Python 3.14+ Compatibility Patch for ChromaDB / Pydantic v1
try:
    import pydantic.v1.fields as _pv1_fields
    _orig_set_default_and_type = _pv1_fields.ModelField._set_default_and_type

    def _safe_set_default_and_type(self):
        if getattr(self, "type_", None) is _pv1_fields.Undefined:
            self.type_ = object
            self.outer_type_ = object
            self.annotation = object
        return _orig_set_default_and_type(self)

    _pv1_fields.ModelField._set_default_and_type = _safe_set_default_and_type
except Exception:
    pass

# Sync Streamlit Cloud secrets into environment if running on Streamlit Community Cloud
try:
    import streamlit as _st
    if hasattr(_st, "secrets"):
        for _k, _v in _st.secrets.items():
            if isinstance(_v, str) and _k not in os.environ:
                os.environ[_k] = _v
except Exception:
    pass


class Settings(BaseSettings):
    """Application Settings"""

    # ==========================================================
    # Application
    # ==========================================================
    APP_NAME: str = "ArchitectAI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    DEBUG: bool = True

    # ==========================================================
    # LLM Provider
    # ==========================================================
    LLM_PROVIDER: str = "groq"

    # ==========================================================
    # Groq Configuration
    # ==========================================================
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "qwen/qwen3.8-27b"
    MODEL_NAME: str = "qwen/qwen3.8-27b"

    # ==========================================================
    # Gemini Configuration (Optional)
    # ==========================================================
    GOOGLE_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-2.5-flash"

    # ==========================================================
    # OpenAI Configuration (Optional)
    # ==========================================================
    OPENAI_API_KEY: str = ""

    OPENAI_MODEL: str = "gpt-4o-mini"

    # ==========================================================
    # Anthropic Configuration (Optional)
    # ==========================================================
    ANTHROPIC_API_KEY: str = ""

    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"

    # ==========================================================
    # Ollama Configuration (Local)
    # ==========================================================
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"

    OLLAMA_MODEL: str = "llama3.2"

    # ==========================================================
    # Testing & Mock Mode
    # ==========================================================
    MOCK_LLM: bool = False

    # ==========================================================
    # Model Settings
    # ==========================================================
    MODEL_TEMPERATURE: float = 0.3

    MAX_OUTPUT_TOKENS: int = 8192

    # ==========================================================
    # Tavily
    # ==========================================================
    TAVILY_API_KEY: str = ""

    # ==========================================================
    # Streamlit
    # ==========================================================
    STREAMLIT_SERVER_PORT: int = 8501

    # ==========================================================
    # ChromaDB
    # ==========================================================
    CHROMA_DB_PATH: str = "./data/chroma_db"

    # ==========================================================
    # Output Directories
    # ==========================================================
    REPORT_OUTPUT_DIR: str = "./outputs/reports"

    DIAGRAM_OUTPUT_DIR: str = "./outputs/diagrams"

    EXPORT_OUTPUT_DIR: str = "./outputs/exports"

    # ==========================================================
    # Retry
    # ==========================================================
    MAX_RETRIES: int = 3

    REQUEST_TIMEOUT: int = 120

    # ==========================================================
    # Logging
    # ==========================================================
    LOG_LEVEL: str = "INFO"

    LOG_FILE: str = "logs/architect_ai.log"

    # ==========================================================
    # FastAPI
    # ==========================================================
    API_HOST: str = "0.0.0.0"

    API_PORT: int = 8000

    # ==========================================================
    # GitHub
    # ==========================================================
    GITHUB_TOKEN: str = ""

    # ==========================================================
    # Pydantic Configuration
    # ==========================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    def get_active_provider(self) -> str:
        """
        Determines the active provider based on configuration and available keys.
        Falls back to alternatives if the primary provider lacks credentials.
        """
        if self.MOCK_LLM:
            return "mock"

        provider = self.LLM_PROVIDER.lower().strip()

        def _has_key(key: str | None) -> bool:
            return bool(key and isinstance(key, str) and key.strip())

        # If primary provider has a key, use it
        if provider == "groq" and _has_key(self.GROQ_API_KEY):
            return "groq"
        if provider in ("google", "gemini") and _has_key(self.GOOGLE_API_KEY):
            return "gemini"
        if provider == "openai" and _has_key(self.OPENAI_API_KEY):
            return "openai"
        if provider == "anthropic" and _has_key(self.ANTHROPIC_API_KEY):
            return "anthropic"
        if provider == "ollama":
            return "ollama"

        # Fallbacks: if default provider lacks key, check if alternatives have keys configured
        if provider == "groq":
            if _has_key(self.GOOGLE_API_KEY):
                return "gemini"
            if _has_key(self.OPENAI_API_KEY):
                return "openai"
            if _has_key(self.ANTHROPIC_API_KEY):
                return "anthropic"

        # Return configured provider even if key is missing (caller will handle error cleanly)
        return provider

    def has_valid_api_key(self) -> bool:
        """Checks if the active provider has valid credentials configured."""
        if self.MOCK_LLM:
            return True
        provider = self.get_active_provider()
        if provider == "groq":
            return bool(self.GROQ_API_KEY and self.GROQ_API_KEY.strip())
        if provider == "gemini":
            return bool(self.GOOGLE_API_KEY and self.GOOGLE_API_KEY.strip())
        if provider == "openai":
            return bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY.strip())
        if provider == "anthropic":
            return bool(self.ANTHROPIC_API_KEY and self.ANTHROPIC_API_KEY.strip())
        if provider == "ollama":
            return True
        return False

    def get_active_model(self) -> str:
        """Returns the model string for the active provider."""
        provider = self.get_active_provider()
        if provider == "mock":
            provider = self.LLM_PROVIDER.lower().strip()

        if provider == "groq":
            return self.GROQ_MODEL or self.MODEL_NAME
        if provider in ("google", "gemini"):
            return self.GEMINI_MODEL
        if provider == "openai":
            return self.OPENAI_MODEL
        if provider == "anthropic":
            return self.ANTHROPIC_MODEL
        if provider == "ollama":
            return self.OLLAMA_MODEL
        return self.MODEL_NAME

    def switch_model(self, model_key: str) -> None:
        """
        Dynamically route between models and providers.
        """
        key = model_key.strip().lower()
        if "claude" in key or "anthropic" in key:
            self.LLM_PROVIDER = "anthropic"
            self.ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"
        elif "gpt-4o-mini" in key:
            self.LLM_PROVIDER = "openai"
            self.OPENAI_MODEL = "gpt-4o-mini"
        elif "gpt-4" in key or "openai" in key:
            self.LLM_PROVIDER = "openai"
            self.OPENAI_MODEL = "gpt-4o"
        elif "gemini" in key or "google" in key or "flash" in key:
            self.LLM_PROVIDER = "gemini"
            self.GEMINI_MODEL = "gemini-2.5-flash"
        elif "ollama" in key or "llama" in key or "local" in key:
            self.LLM_PROVIDER = "ollama"
            self.OLLAMA_MODEL = "llama3.2"
        elif "groq" in key or "qwen" in key:
            self.LLM_PROVIDER = "groq"
            self.GROQ_MODEL = "qwen/qwen3.8-27b"
            self.MODEL_NAME = "qwen/qwen3.8-27b"


# ==========================================================
# Global Settings Object
# ==========================================================

settings = Settings()


# ==========================================================
# Create Required Directories
# ==========================================================

Path(settings.CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
Path(settings.REPORT_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.DIAGRAM_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.EXPORT_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(exist_ok=True)


# ==========================================================
# Helper Functions
# ==========================================================

def is_development() -> bool:
    return settings.APP_ENV.lower() == "development"


def is_production() -> bool:
    return settings.APP_ENV.lower() == "production"


def project_info() -> dict:
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "provider": settings.LLM_PROVIDER,
        "model": settings.MODEL_NAME
        if settings.LLM_PROVIDER == "groq"
        else settings.GEMINI_MODEL,
        "debug": settings.DEBUG,
    }