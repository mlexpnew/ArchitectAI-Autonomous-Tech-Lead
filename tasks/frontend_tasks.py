"""
Frontend Task

Generate a complete frontend engineering document.
"""

from crewai import Task


def create_frontend_task(
    agent,
    requirements: str,
    architecture: str,
):

    return Task(

        description=f"""
Requirements

{requirements[:1200]}

Architecture

{architecture[:1200]}

Generate a frontend design.

Include only:

1. React Folder Structure

2. Pages

3. Components

4. Routing

5. State Management

6. API Integration

7. UI Libraries

Return Markdown only.
""",

        expected_output=(
            "A complete frontend engineering document in Markdown."
        ),

        agent=agent,
    )