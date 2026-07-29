"""
Architecture Crew

Generates software architecture from requirement documents.
"""

from crewai import Crew
from crewai import Process

from agents.solution_architect import create_solution_architect
from tasks.architecture_task import create_architecture_task

from utils.file_manager import FileManager


class ArchitectureCrew:

    def __init__(self, project_name: str):

        self.project_name = project_name
        self.file_manager = FileManager()

    def run(self):

        # Read Requirement Document
        requirements = self.file_manager.read_document(
            project_name=self.project_name,
            filename="requirements.md",
        )

        if not requirements.strip():
            raise ValueError(
                "requirements.md not found or is empty."
            )

        # Create Agent
        architect = create_solution_architect()

        # Create Task
        architecture_task = create_architecture_task(
            architect,
            requirements,
        )

        # Create Crew
        crew = Crew(

            agents=[
                architect,
            ],

            tasks=[
                architecture_task,
            ],

            process=Process.sequential,

            verbose=True,
        )

        # Execute Crew
        result = crew.kickoff()

        # Save Output
        output_path = self.file_manager.save_document(

            project_name=self.project_name,

            filename="architecture.md",

            content=str(result),
        )

        print("\n✅ Architecture document saved successfully.")
        print(output_path)

        return result