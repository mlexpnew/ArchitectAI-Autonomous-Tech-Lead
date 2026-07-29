"""
Planning Crew

Responsible for transforming an idea into software requirements.
"""

from crewai import Crew
from crewai import Process

from agents.requirement_analyst import create_requirement_analyst
from tasks.requirement_tasks import create_requirement_task

from utils.file_manager import FileManager


class PlanningCrew:

    def __init__(self, project_idea: str):

        self.project_idea = project_idea
        self.file_manager = FileManager()

    def run(self):

        requirement_agent = create_requirement_analyst()

        requirement_task = create_requirement_task(
            requirement_agent,
            self.project_idea,
        )

        crew = Crew(
            agents=[
                requirement_agent,
            ],
            tasks=[
                requirement_task,
            ],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        # Save report automatically
        report_path = self.file_manager.save_timestamped_report(
            project_name="requirement_analysis",
            content=str(result),
        )

        print(f"\n✅ Report saved successfully:")
        print(report_path)

        return result