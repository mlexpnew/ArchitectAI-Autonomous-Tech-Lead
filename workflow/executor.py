"""
Workflow Executor
"""

from plugins.plugin_manager import PluginManager


class WorkflowExecutor:

    def __init__(
        self,
        output_dir: str,
    ):

        self.plugin_manager = PluginManager(
            output_dir,
        )

    def execute(
        self,
        dag,
        entity_name: str,
        fields: list[str],
    ):

        while not dag.finished():

            ready_nodes = dag.ready_nodes()

            if not ready_nodes:

                raise RuntimeError(
                    "Workflow deadlock detected."
                )

            for node in ready_nodes:

                print(f"\n🚀 Executing {node.name}")

                self.plugin_manager.execute(
                    node.plugin,
                    entity_name,
                    fields,
                )

                dag.mark_completed(
                    node.name,
                )

        print("\n✅ Workflow Completed")