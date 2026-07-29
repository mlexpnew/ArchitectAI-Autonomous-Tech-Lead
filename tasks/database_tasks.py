"""
Database Task

Generate a complete database design document.
"""

from crewai import Task


def create_database_task(
    agent,
    requirements: str,
    architecture: str,
):

    return Task(

        description=f"""
Requirements

{requirements}

Architecture

{architecture}

Generate a database design.

Include only:

1. Database Technology

2. Tables

3. Relationships

4. Primary Keys

5. Foreign Keys

6. Indexes

7. Mermaid ER Diagram

Return Markdown only.
""",

        expected_output=(
            "A complete enterprise database design document in Markdown."
        ),

        agent=agent,
    )