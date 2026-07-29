"""
Engineering Crew

Runs one engineering stage at a time.

Supported stages

- requirement
- architecture
- backend
- database
- frontend
"""

from crewai import Crew, Process

from agents.requirement_analyst import create_requirement_analyst
from agents.solution_architect import create_solution_architect
from agents.backend_engineer import create_backend_engineer
from agents.database_architect import create_database_architect
from agents.frontend_engineer import create_frontend_engineer

from tasks.requirement_tasks import create_requirement_task
from tasks.architecture_tasks import create_architecture_task
from tasks.backend_tasks import create_backend_task
from tasks.database_tasks import create_database_task
from tasks.frontend_tasks import create_frontend_task

from utils.file_manager import FileManager


class EngineeringCrew:

    def __init__(
        self,
        project_name: str,
        project_idea: str,
    ):

        self.project_name = project_name
        self.project_idea = project_idea

        self.file_manager = FileManager()

    def _run_single_task(self, agent, task):

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        return crew.kickoff()

    # --------------------------------------------------------
    # Requirement Stage
    # --------------------------------------------------------

    def run_requirement(self):

        agent = create_requirement_analyst()

        task = create_requirement_task(
            agent,
            self.project_idea,
        )

        result = self._run_single_task(agent, task)

        self.file_manager.save_document(
            project_name=self.project_name,
            filename="requirements.md",
            content=str(result),
        )

        print("\n✅ requirements.md generated")

    # --------------------------------------------------------
    # Architecture Stage
    # --------------------------------------------------------

    def run_architecture(self):

        requirements = self.file_manager.read_document(
            self.project_name,
            "requirements.md",
        )

        agent = create_solution_architect()

        task = create_architecture_task(
            agent,
            requirements,
        )

        result = self._run_single_task(agent, task)

        self.file_manager.save_document(
            project_name=self.project_name,
            filename="architecture.md",
            content=str(result),
        )

        print("\n✅ architecture.md generated")

    # --------------------------------------------------------
    # Backend Stage
    # --------------------------------------------------------

    def run_backend(self):

        requirements = self.file_manager.read_document(
            self.project_name,
            "requirements.md",
        )

        architecture = self.file_manager.read_document(
            self.project_name,
            "architecture.md",
        )

        agent = create_backend_engineer()

        task = create_backend_task(
            agent,
            requirements,
            architecture,
        )

        result = self._run_single_task(agent, task)

        self.file_manager.save_document(
            project_name=self.project_name,
            filename="backend.md",
            content=str(result),
        )

        print("\n✅ backend.md generated")

    # --------------------------------------------------------
    # Database Stage
    # --------------------------------------------------------

    def run_database(self):

        requirements = self.file_manager.read_document(
            self.project_name,
            "requirements.md",
        )

        architecture = self.file_manager.read_document(
            self.project_name,
            "architecture.md",
        )

        agent = create_database_architect()

        task = create_database_task(
            agent,
            requirements,
            architecture,
        )

        result = self._run_single_task(agent, task)

        self.file_manager.save_document(
            project_name=self.project_name,
            filename="database.md",
            content=str(result),
        )

        print("\n✅ database.md generated")

    # --------------------------------------------------------
    # Frontend Stage
    # --------------------------------------------------------

    def run_frontend(self):

        requirements = self.file_manager.read_document(
            self.project_name,
            "requirements.md",
        )

        architecture = self.file_manager.read_document(
            self.project_name,
            "architecture.md",
        )

        agent = create_frontend_engineer()

        task = create_frontend_task(
            agent,
            requirements,
            architecture,
        )

        result = self._run_single_task(agent, task)

        self.file_manager.save_document(
            project_name=self.project_name,
            filename="frontend.md",
            content=str(result),
        )

        print("\n✅ frontend.md generated")

    # --------------------------------------------------------
    # Main Runner
    # --------------------------------------------------------

    def run(self, stage: str):

        stage = stage.lower()

        if stage == "requirement":
            self.run_requirement()

        elif stage == "architecture":
            self.run_architecture()

        elif stage == "backend":
            self.run_backend()

        elif stage == "database":
            self.run_database()

        elif stage == "frontend":
            self.run_frontend()

        else:
            raise ValueError(
                f"Unknown stage: {stage}"
            )