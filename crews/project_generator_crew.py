from crewai import Crew, Process

from agents.project_generator import (
    create_project_generator,
)

from tasks.project_generator_tasks import (
    create_project_generator_task,
)


class ProjectGeneratorCrew:

    def run(self):

        agent = create_project_generator()

        task = create_project_generator_task(agent)

        crew = Crew(

            agents=[agent],

            tasks=[task],

            process=Process.sequential,

            verbose=True,
        )

        return crew.kickoff()