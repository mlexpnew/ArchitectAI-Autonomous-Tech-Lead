"""
Workflow Node
"""

from dataclasses import dataclass, field


@dataclass
class WorkflowNode:

    name: str

    plugin: str

    dependencies: list[str] = field(default_factory=list)

    completed: bool = False