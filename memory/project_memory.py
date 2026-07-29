"""
Project Memory
"""

from dataclasses import dataclass, field


@dataclass
class ProjectMemory:

    entities: dict = field(default_factory=dict)

    generated_files: list[str] = field(default_factory=list)

    completed_plugins: list[str] = field(default_factory=list)

    failed_plugins: list[str] = field(default_factory=list)

    project_metadata: dict = field(default_factory=dict)