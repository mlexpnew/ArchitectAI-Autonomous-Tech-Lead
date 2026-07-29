"""
Backend Engineer Agent

Designs and generates the backend architecture for the software system.
"""

from crewai import Agent

from config.llm import llm


def create_backend_engineer():
    """
    Create Backend Engineer Agent.
    """

    return Agent(
        role="Senior Backend Engineer",

        goal=(
            "Design a scalable, secure and production-ready backend "
            "architecture from software requirements and system architecture."
        ),

        backstory=(
            "You are a Senior Python Backend Engineer with more than "
            "12 years of experience building enterprise applications "
            "using FastAPI, Flask, PostgreSQL, Redis, Docker, "
            "Microservices, REST APIs, Authentication, CI/CD and Cloud."
        ),

        llm=llm,

        verbose=True,

        allow_delegation=False,
    )