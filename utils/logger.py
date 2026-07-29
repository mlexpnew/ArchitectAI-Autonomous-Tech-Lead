"""
Application Logger

ArchitectAI - Autonomous Tech Lead

Provides centralized logging for the entire application.
"""

import sys
from pathlib import Path

from loguru import logger

from config.settings import settings


LOG_PATH = Path(settings.LOG_FILE)

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


logger.remove()


# -------------------------------------------------------
# Console Logger
# -------------------------------------------------------

logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)


# -------------------------------------------------------
# File Logger
# -------------------------------------------------------

logger.add(
    settings.LOG_FILE,
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level=settings.LOG_LEVEL,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level:<8} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)


# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------

def log_startup():
    """Log application startup information."""

    logger.info("=" * 70)
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Version      : {settings.APP_VERSION}")
    logger.info(f"Environment  : {settings.APP_ENV}")
    logger.info(f"Gemini Model : {settings.GEMINI_MODEL}")
    logger.info("=" * 70)


def log_agent_start(agent_name: str):
    """Log agent execution start."""

    logger.info(f"🚀 Starting Agent: {agent_name}")


def log_agent_end(agent_name: str):
    """Log agent execution completion."""

    logger.success(f"✅ Finished Agent: {agent_name}")


def log_task(task_name: str):
    """Log task execution."""

    logger.info(f"📌 Task: {task_name}")


def log_error(error: Exception):
    """Log application errors."""

    logger.exception(error)


def log_user_prompt(prompt: str):
    """Log user input."""

    logger.info(f"User Prompt: {prompt}")


def log_report_generated():
    """Log report completion."""

    logger.success("📄 Engineering report generated successfully.")