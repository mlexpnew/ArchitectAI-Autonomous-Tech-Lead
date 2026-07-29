"""
Artifact Dependency Graph
"""

import json
from pathlib import Path

from graph.dependency_node import DependencyNode


class ArtifactGraph:

    def __init__(
        self,
        output_dir: str,
    ):

        self.graph_file = (
            Path(output_dir)
            / ".artifact_graph.json"
        )

        self.nodes = {}

        self.load()

    def add_node(
        self,
        node: DependencyNode,
    ):

        self.nodes[node.name] = node

        self.save()

    def add_dependency(
        self,
        parent: str,
        child: str,
    ):

        if parent not in self.nodes:
            return

        if child not in self.nodes:
            return

        if child not in self.nodes[parent].dependents:

            self.nodes[parent].dependents.append(
                child,
            )

        if parent not in self.nodes[child].dependencies:

            self.nodes[child].dependencies.append(
                parent,
            )

        self.save()

    def affected(
        self,
        name: str,
    ):

        affected = set()

        queue = [name]

        while queue:

            current = queue.pop(0)

            if current in affected:
                continue

            affected.add(current)

            queue.extend(
                self.nodes[current].dependents
            )

        return sorted(affected)

    def save(self):

        data = {}

        for name, node in self.nodes.items():

            data[name] = {

                "plugin": node.plugin,

                "file_path": node.file_path,

                "dependencies": node.dependencies,

                "dependents": node.dependents,

                "prompt_hash": node.prompt_hash,

            }

        self.graph_file.write_text(

            json.dumps(
                data,
                indent=4,
            ),

            encoding="utf-8",

        )

    def load(self):

        if not self.graph_file.exists():
            return

        data = json.loads(
            self.graph_file.read_text(
                encoding="utf-8"
            )
        )

        for name, item in data.items():

            self.nodes[name] = DependencyNode(

                name=name,

                plugin=item["plugin"],

                file_path=item["file_path"],

                dependencies=item["dependencies"],

                dependents=item["dependents"],

                prompt_hash=item.get(
                    "prompt_hash",
                    "",
                ),

            )