"""
Architecture Task

Generates software architecture from software requirements.
"""

from crewai import Task


def create_architecture_task(agent, requirements):

    return Task(

        description=f"""
You are the Solution Architect.

Requirements:

{requirements}

Generate a concise software architecture document.

Include only:

1. Executive Summary

2. Recommended Tech Stack

3. High-Level Architecture

4. Main Components

5. Database Choice

6. API Design

7. Deployment Overview

8. Mermaid Architecture Diagram

Return the response in Markdown format.
""",

        expected_output=(
            "A professional software architecture document in Markdown."
        ),

        agent=agent,
    )