"""
Project Configuration

ArchitectAI - Autonomous Tech Lead

Centralized application configuration using Pydantic Settings.
Supports multiple LLM providers (Groq, Gemini, OpenAI, Ollama).
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    MODEL_NAME: str = "llama-3.3-70b-versatile"

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
        if provider == "ollama":
            return "ollama"

        # Fallbacks: check if any other provider has a valid key configured
        if _has_key(self.GROQ_API_KEY):
            return "groq"
        if _has_key(self.GOOGLE_API_KEY):
            return "gemini"
        if _has_key(self.OPENAI_API_KEY):
            return "openai"

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
        if provider == "ollama":
            return True
        return False

    def get_active_model(self) -> str:
        """Returns the model string for the active provider."""
        provider = self.get_active_provider()
        if provider == "groq":
            return self.MODEL_NAME
        if provider == "gemini":
            return self.GEMINI_MODEL
        if provider == "openai":
            return self.OPENAI_MODEL
        if provider == "ollama":
            return self.OLLAMA_MODEL
        return self.MODEL_NAME


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