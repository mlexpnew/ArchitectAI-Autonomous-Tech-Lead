"""
Project Task
"""

from dataclasses import dataclass, field


@dataclass
class ProjectTask:

    agent: str

    title: str

    description: str

    priority: int = 1

    depends_on: list[str] = field(default_factory=list)