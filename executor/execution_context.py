"""
Execution Context

Stores project state during execution.
"""

from dataclasses import dataclass, field


@dataclass
class ExecutionContext:

    project_name: str

    project_root: str

    requirements: str

    current_step: int = 0

    generated_files: list[str] = field(default_factory=list)

    completed_tasks: list[str] = field(default_factory=list)

    failed_tasks: list[str] = field(default_factory=list)