"""
Shared Workspace

Central in-memory workspace used by ArchitectAI agents
to publish, retrieve, and share generated artifacts.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class WorkspaceArtifact:
    """
    Represents an artifact published by an agent.
    """

    name: str
    category: str
    author: str
    content: Any
    version: int = 1
    created_at: datetime | None = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class SharedWorkspace:
    """
    Shared communication and artifact storage layer
    for all ArchitectAI agents.
    """

    def __init__(self):

        self.artifacts = {}

    # ---------------------------------------------------------
    # New Agent Artifact API
    # ---------------------------------------------------------

    def publish(
        self,
        name: str,
        category: str,
        author: str,
        content: Any,
    ):
        """
        Publish or update an artifact.
        """

        existing = self.artifacts.get(name)

        version = 1

        if isinstance(existing, WorkspaceArtifact):
            version = existing.version + 1

        artifact = WorkspaceArtifact(
            name=name,
            category=category,
            author=author,
            content=content,
            version=version,
        )

        self.artifacts[name] = artifact

        print(
            f"📦 Published: {name} "
            f"[{category}] "
            f"by {author} "
            f"(v{version})"
        )

        return artifact

    def get(
        self,
        name: str,
    ):
        """
        Retrieve artifact by name.
        """

        return self.artifacts.get(name)

    def list(self):
        """
        Return all published artifacts.
        """

        return list(
            self.artifacts.values()
        )

    # ---------------------------------------------------------
    # Legacy Workspace API
    # Keep for backward compatibility
    # ---------------------------------------------------------

    def save(
        self,
        category: str,
        name: str,
        value: Any,
    ):
        """
        Legacy category-based storage.
        """

        category_store = self.artifacts.setdefault(
            category,
            {},
        )

        if not isinstance(category_store, dict):
            category_store = {}
            self.artifacts[category] = category_store

        category_store[name] = value

        return value

    def load(
        self,
        category: str,
        name: str,
    ):
        """
        Load legacy category-based value.
        """

        category_store = self.artifacts.get(
            category,
            {},
        )

        if not isinstance(category_store, dict):
            return None

        return category_store.get(name)

    def get_category(
        self,
        category: str,
    ):
        """
        Return legacy artifact category.
        """

        category_store = self.artifacts.get(
            category,
            {},
        )

        if isinstance(category_store, dict):
            return category_store

        return {}

    def categories(self):
        """
        Return available artifact categories.
        """

        return [
            key
            for key, value in self.artifacts.items()
            if isinstance(value, dict)
        ]

    def clear(self):
        """
        Clear complete workspace.
        """

        self.artifacts.clear()