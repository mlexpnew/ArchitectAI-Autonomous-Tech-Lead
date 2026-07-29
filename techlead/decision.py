from dataclasses import dataclass, field


@dataclass
class Decision:

    continue_project: bool

    retry_agents: list[str] = field(default_factory=list)

    new_tasks: list[dict] = field(default_factory=list)

    message: str = ""