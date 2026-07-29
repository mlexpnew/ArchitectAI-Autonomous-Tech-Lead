"""
QA Agent
"""

from agents.base_agent import BaseAgent


class QAAgent(BaseAgent):

    @property
    def name(self):
        return "qa"

    def execute(self, project):

        print("🧪 QA Agent")

        if not self.has_tasks():

            print("No QA tasks.")

            return

        for task in self.get_tasks():

            print(f" • {task}")

        print()

        print("Artifacts")

        for artifact in self.list_artifacts():

            print(f"Testing -> {artifact.name}")

        self.clear_tasks()

        print("✅ QA Finished")