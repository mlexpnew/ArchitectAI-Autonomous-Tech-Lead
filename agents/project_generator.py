"""
Project Generator Agent
"""

from crewai import Agent

from config.llm import llm


def create_project_generator():

    return Agent(

        role="Project Generator",

        goal="Generate production-ready project structure.",

        backstory=(
            "You are an experienced software architect who creates "
            "production-ready project structures for enterprise applications."
        ),

        llm=llm,

        verbose=True,

        allow_delegation=False,
    )