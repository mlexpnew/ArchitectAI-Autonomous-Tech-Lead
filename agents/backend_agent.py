"""
Backend Agent
"""

from agents.base_agent import BaseAgent


class BackendAgent(BaseAgent):

    @property
    def name(self):
        return "backend"

    def execute(self, project):

        print("🏗 Backend Agent")

        print(f"Project : {project}")

        if not self.has_tasks():

            print("No backend tasks.")

            return

        for task in self.get_tasks():

            print(f" • {task}")

        service_code = """
from fastapi import APIRouter

router = APIRouter()


@router.get("/patients")
def get_patients():
    return {"message": "Patient API"}
"""

        artifact = self.publish_artifact(

            name="patient_service.py",

            category="service",

            content=service_code,

        )

        print()

        print("📦 Published Artifact")

        print(f"Name     : {artifact.name}")
        print(f"Version  : {artifact.version}")

        self.send(

            receiver="documentation",

            title="Backend Completed",

            content=artifact.name,

        )

        self.send(

            receiver="qa",

            title="Backend Completed",

            content=artifact.name,

        )

        self.send(

            receiver="security",

            title="Backend Completed",

            content=artifact.name,

        )

        self.clear_tasks()

        print("✅ Backend Agent Finished")