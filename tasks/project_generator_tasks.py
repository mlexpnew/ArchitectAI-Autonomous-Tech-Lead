from crewai import Task


def create_project_generator_task(agent):

    return Task(

        description="""
Review the generated documents and recommend the complete
software project directory structure.

Include:

1. Backend folders

2. Frontend folders

3. Database folder

4. Docker

5. Tests

6. Docs

Return Markdown.
""",

        expected_output="Project folder structure",

        agent=agent,
    )