from agents.base_agent import BaseAgent


class FrontendAgent(BaseAgent):
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

        return "frontend"

    def execute(
        self,
        project,
    ):

        print("🎨 Frontend Agent")

        for task in self.tasks:

            print(" •", task)