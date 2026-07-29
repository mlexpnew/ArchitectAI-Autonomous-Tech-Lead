"""
Agent Manager
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

        print("Loaded Agents:", list(self.agents.keys()))

    def get(self, name):

        return self.agents.get(name)

    def execute_all(self, project):

        print("Executing agents...")

        for name, agent in self.agents.items():

            print(f"Running {name}")

            agent.execute(project)

        print("Done")