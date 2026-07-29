"""
Base Agent
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(
        self,
        workspace,
        bus,
    ):
        self.workspace = workspace
        self.bus = bus
        self.tasks = []

    @property
    @abstractmethod
    def name(self):
        """Unique agent name"""
        pass

    def add_task(self, task):
        self.tasks.append(task)

    def clear_tasks(self):
        self.tasks.clear()

    def get_tasks(self):
        return list(self.tasks)

    def has_tasks(self):
        return len(self.tasks) > 0

    # ------------------------------------------------------------------
    # Artifact Helpers
    # ------------------------------------------------------------------

    def publish_artifact(
        self,
        name,
        category,
        content,
    ):
        """
        Publish an artifact to the shared workspace.
        """

        return self.workspace.publish(
            name=name,
            category=category,
            author=self.name,
            content=content,
        )

    def get_artifact(self, name):
        """
        Load a specific artifact.
        """

        return self.workspace.get(name)

    def list_artifacts(self):
        """
        List all available artifacts.
        """

        return self.workspace.list()

    # ------------------------------------------------------------------
    # Communication Helpers
    # ------------------------------------------------------------------

    def send(
        self,
        receiver,
        title,
        content,
    ):
        self.bus.send(
            sender=self.name,
            receiver=receiver,
            title=title,
            content=content,
        )

    def inbox(self):
        return self.bus.inbox(self.name)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    @abstractmethod
    def execute(self, project):
        """
        Execute assigned tasks.
        """
        pass