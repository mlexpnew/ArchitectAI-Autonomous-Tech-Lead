"""
Parallel Workflow Executor
"""

from concurrent.futures import ThreadPoolExecutor

from plugins.plugin_manager import PluginManager


class ParallelWorkflowExecutor:

    def __init__(
        self,
        output_dir: str,
        max_workers: int = 4,
    ):

        self.plugin_manager = PluginManager(output_dir)

        self.max_workers = max_workers

    def _run(
        self,
        node,
        entity_name,
        fields,
    ):

        print(f"🚀 {node.name}")

        self.plugin_manager.execute(
            node.plugin,
            entity_name,
            fields,
        )

        return node.name

    def execute(
        self,
        dag,
        entity_name,
        fields,
    ):

        while not dag.finished():

            ready = dag.ready_nodes()

            if not ready:

                raise RuntimeError(
                    "Workflow deadlock detected."
                )

            with ThreadPoolExecutor(
                max_workers=self.max_workers,
            ) as executor:

                futures = [

                    executor.submit(

                        self._run,

                        node,

                        entity_name,

                        fields,

                    )

                    for node in ready

                ]

                for future in futures:

                    dag.mark_completed(
                        future.result()
                    )

        print("\n✅ Parallel Workflow Completed")