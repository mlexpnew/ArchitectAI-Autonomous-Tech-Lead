"""
Database Architect Agent

Designs scalable database architecture for enterprise software systems.
"""

from crewai import Agent

from config.llm import llm


def create_database_architect():
    """
    Create Database Architect Agent.
    """

    return Agent(

        role="Senior Database Architect",

        goal=(
            "Design a scalable, secure, high-performance database "
            "architecture based on software requirements."
        ),

        backstory=(
            "You are a Senior Database Architect with over 15 years "
            "of experience designing enterprise databases using "
            "PostgreSQL, MySQL, MongoDB, Redis, Cassandra and Vector "
            "Databases. You specialize in database normalization, "
            "query optimization, indexing, high availability, "
            "replication, partitioning, backups and security."
        ),

        llm=llm,

        verbose=True,

        allow_delegation=False,
    )