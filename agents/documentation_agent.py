"""
Documentation Agent
"""

from agents.base_agent import BaseAgent


class DocumentationAgent(BaseAgent):

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
        return "documentation"

    def execute(
        self,
        project,
    ):

        print("📄 Documentation Agent")

        # -----------------------------
        # Read Messages
        # -----------------------------

        inbox = self.inbox()

        if inbox:

            print("\n📥 Messages")

            for msg in inbox:

                print(f"From    : {msg['sender']}")
                print(f"Title   : {msg['title']}")
                print(f"Content : {msg['content']}")
                print("-" * 40)

        else:

            print("No messages received.")

        # -----------------------------
        # Read Shared Artifacts
        # -----------------------------

        print("\n📦 Shared Workspace")

        services = self.workspace.get_category("services")

        if not services:

            print("No services found.")

            return

        for artifact in services.values():

            print(f"Name     : {artifact.name}")
            print(f"Author   : {artifact.author}")
            print(f"Version  : {artifact.version}")
            print(f"Category : {artifact.category}")
            print("Content")
            print(artifact.content)
            print("-" * 50)

        print("✅ Documentation Agent Finished")