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