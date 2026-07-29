"""
ArchitectAI Workflow Engine

Controls execution order and dependencies
between autonomous engineering agents.
"""

from typing import Dict, List


class WorkflowEngine:

    DEFAULT_WORKFLOW = [
        "database",
        "backend",
        "frontend",
        "security",
        "qa",
        "devops",
        "documentation",
    ]

    def __init__(
        self,
        agent_manager,
    ):
        self.agent_manager = agent_manager

    def execute(
        self,
        project,
        workflow: List[str] | None = None,
    ):
        """
        Execute agents in workflow order.
        """

        execution_order = (
            workflow
            if workflow is not None
            else self.DEFAULT_WORKFLOW
        )

        results: Dict[str, object] = {}

        print("\n" + "=" * 60)
        print("🚀 ArchitectAI Workflow Started")
        print("=" * 60)

        for agent_name in execution_order:

            agent = self.agent_manager.get(
                agent_name
            )

            if agent is None:
                raise ValueError(
                    f"Agent '{agent_name}' "
                    "is not registered."
                )

            print(
                f"\n▶ Running Agent: "
                f"{agent_name}"
            )

            try:
                result = agent.execute(
                    project
                )

                results[agent_name] = result

                print(
                    f"✅ {agent_name} completed"
                )

            except Exception as exc:

                print(
                    f"❌ {agent_name} failed: "
                    f"{exc}"
                )

                raise

        print("\n" + "=" * 60)
        print("✅ ArchitectAI Workflow Completed")
        print("=" * 60)

        return results