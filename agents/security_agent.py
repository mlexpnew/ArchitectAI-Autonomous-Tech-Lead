from agents.base_agent import BaseAgent


class SecurityAgent(BaseAgent):
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

        return "security"

    def execute(
        self,
        project,
    ):

        print("🔒 Security Agent")

        for task in self.tasks:

            print(" •", task)