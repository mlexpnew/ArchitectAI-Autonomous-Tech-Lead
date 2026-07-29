"""
Dependency Node
"""

from dataclasses import dataclass, field


@dataclass
class DependencyNode:

    name: str

    plugin: str

    file_path: str

    dependencies: list[str] = field(default_factory=list)

    dependents: list[str] = field(default_factory=list)

    prompt_hash: str = ""