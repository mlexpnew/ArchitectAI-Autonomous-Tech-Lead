"""
Backend Task

Generate a complete backend design document.
"""

from crewai import Task


def create_backend_task(
    agent,
    requirements: str,
    architecture: str,
):

    return Task(
        agent=agent,
        description=f"""
Requirements

{requirements}

Architecture

{architecture}

Generate a backend design.

Include only:

1. Backend Folder Structure

2. FastAPI Modules

3. Authentication Strategy

4. API Endpoints

5. Database Integration

6. Error Handling

7. Recommended Python Packages

Return Markdown only.
""",
        expected_output="A complete backend engineering document.",
    )