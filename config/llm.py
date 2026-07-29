"""
LLM Configuration
"""

from crewai import LLM
from config.settings import settings

llm = LLM(
    model=f"groq/{settings.MODEL_NAME}",
    api_key=settings.GROQ_API_KEY,
    temperature=settings.MODEL_TEMPERATURE,
)