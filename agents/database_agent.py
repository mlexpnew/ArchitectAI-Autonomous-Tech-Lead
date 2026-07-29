from agents.base_agent import BaseAgent


class DatabaseAgent(BaseAgent):
     def __init__(
        self,
        workspace,
        bus,
    ):
        super().__init__(
            workspace,
            bus,
        )

     @property
     def name(self):
        return "database"

     def execute(
        self,
        project,
    ):

        print("🗄 Database Agent")

        for task in self.tasks:

            print(" •", task)