"""
Workflow Cache
"""

import json
from pathlib import Path

from workflow.dag import WorkflowDAG
from workflow.node import WorkflowNode


class WorkflowCache:

    def __init__(
        self,
        output_dir: str,
    ):

        self.cache_file = (
            Path(output_dir)
            / ".workflow_cache.json"
        )

    def exists(self):

        return self.cache_file.exists()

    def save(
        self,
        dag: WorkflowDAG,
    ):

        data = []

        for node in dag.nodes.values():

            data.append(
                {
                    "name": node.name,
                    "plugin": node.plugin,
                    "dependencies": node.dependencies,
                }
            )

        self.cache_file.write_text(

            json.dumps(
                data,
                indent=4,
            ),

            encoding="utf-8",

        )

    def load(self):

        data = json.loads(
            self.cache_file.read_text(
                encoding="utf-8"
            )
        )

        dag = WorkflowDAG()

        for node in data:

            dag.add_node(

                WorkflowNode(

                    name=node["name"],

                    plugin=node["plugin"],

                    dependencies=node["dependencies"],

                )

            )

        return dag