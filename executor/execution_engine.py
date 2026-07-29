"""
Execution Engine
"""

from executor.task_dispatcher import TaskDispatcher


class ExecutionEngine:

    def __init__(
        self,
        output_dir: str,
    ):

        self.dispatcher = TaskDispatcher(
            output_dir,
        )

    def execute(
        self,
        tasks,
        entity_name: str,
        fields: list[str],
    ):

        print("\n" + "=" * 70)
        print("ArchitectAI Execution Engine")
        print("=" * 70)

        for task in tasks:

            self.dispatcher.dispatch(
                task,
                entity_name,
                fields,
            )

        print("\n🎉 Execution Completed")