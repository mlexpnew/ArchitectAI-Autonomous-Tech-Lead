from agents.base_agent import BaseAgent


class DevOpsAgent(BaseAgent):
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

        return "devops"

    def execute(
        self,
        project,
    ):

        print("🚀 DevOps Agent")

        for task in self.tasks:

            print(" •", task)