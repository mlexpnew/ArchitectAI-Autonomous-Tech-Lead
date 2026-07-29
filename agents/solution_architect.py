"""
Solution Architect Agent

Designs scalable software architecture from business requirements.
"""

from crewai import Agent

from config.llm import llm


def create_solution_architect():
    """
    Create the Solution Architect Agent.
    """

    return Agent(
        role="Senior Solution Architect",

        goal=(
            "Design a scalable, secure, production-ready software "
            "architecture based on the business requirements."
        ),

        backstory=(
            "You are a Principal Solution Architect with over 15 years "
            "of experience designing enterprise software systems. "
            "You specialize in distributed systems, cloud architecture, "
            "microservices, AI applications, security, scalability, "
            "database design, and DevOps."
        ),

        llm=llm,

        verbose=True,

        allow_delegation=False,
    )