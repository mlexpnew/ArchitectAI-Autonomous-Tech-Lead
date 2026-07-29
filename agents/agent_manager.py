"""
Agent Manager

Central registry and orchestration entry point
for ArchitectAI autonomous agents.
"""

from agents.backend_agent import BackendAgent
from agents.database_agent import DatabaseAgent
from agents.devops_agent import DevOpsAgent
from agents.documentation_agent import DocumentationAgent
from agents.frontend_agent import FrontendAgent
from agents.qa_agent import QAAgent
from agents.security_agent import SecurityAgent

from collaboration.workspace import SharedWorkspace
from collaboration.message_bus import MessageBus


class AgentManager:

    def __init__(self):

        print("Creating AgentManager")

        self.workspace = SharedWorkspace()
        self.bus = MessageBus()

        self.agents = {
            "backend": BackendAgent(
                self.workspace,
                self.bus,
            ),
            "frontend": FrontendAgent(
                self.workspace,
                self.bus,
            ),
            "database": DatabaseAgent(
                self.workspace,
                self.bus,
            ),
            "devops": DevOpsAgent(
                self.workspace,
                self.bus,
            ),
            "qa": QAAgent(
                self.workspace,
                self.bus,
            ),
            "security": SecurityAgent(
                self.workspace,
                self.bus,
            ),
            "documentation": DocumentationAgent(
                self.workspace,
                self.bus,
            ),
        }

        print(
            "Loaded Agents:",
            list(self.agents.keys()),
        )

    def get(
        self,
        name: str,
    ):
        """
        Return registered agent by name.
        """

        return self.agents.get(name)

    def list_agents(self):
        """
        Return registered agent names.
        """

        return list(
            self.agents.keys()
        )

    def execute_agent(
        self,
        name: str,
        project,
    ):
        """
        Execute one specific agent.
        """

        agent = self.get(name)

        if agent is None:
            raise ValueError(
                f"Agent '{name}' is not registered."
            )

        print(
            f"\n▶ Executing agent: {name}"
        )

        return agent.execute(project)

    def execute_all(
        self,
        project,
    ):
        """
        Legacy execution method.

        Executes every registered agent.
        """

        print("\nExecuting all agents...")

        results = {}

        for name, agent in self.agents.items():

            print(
                f"\n▶ Running {name}"
            )

            results[name] = agent.execute(
                project
            )

        print("\n✅ All agents completed")

        return results

    def execute_workflow(
        self,
        project,
        workflow=None,
    ):
        """
        Execute agents through WorkflowEngine.
        """

        # Local import avoids circular imports.
        from orchestration.workflow_engine import (
            WorkflowEngine,
        )

        engine = WorkflowEngine(self)

        return engine.execute(
            project=project,
            workflow=workflow,
        )