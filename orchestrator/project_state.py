from dataclasses import dataclass, field


@dataclass
class ProjectState:

    project_name: str

    completed: list[str] = field(default_factory=list)

    failed: list[str] = field(default_factory=list)

    current: str = ""

    status: str = "Planning"