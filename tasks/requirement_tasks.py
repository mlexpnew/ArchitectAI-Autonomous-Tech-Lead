"""
Requirement Tasks
"""

from crewai import Task


def create_requirement_task(agent, project_idea: str):

    description=f"""
Project Idea

{project_idea}

Generate software requirements.

Include only:

1. Executive Summary

2. Functional Requirements

3. Non-Functional Requirements

4. User Roles

5. Core Features

Return Markdown only.
"""

    expected_output = """
A structured Markdown report including:

- Executive Summary
- Business Problem
- Functional Requirements
- Non Functional Requirements
- User Personas
- User Stories
- Acceptance Criteria
- Risks
"""

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )