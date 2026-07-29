"""
Change Detector
"""

import hashlib
from pathlib import Path

from graph.artifact_graph import ArtifactGraph


class ChangeDetector:

    def __init__(
        self,
        output_dir: str,
    ):

        self.graph = ArtifactGraph(output_dir)

    @staticmethod
    def hash_file(
        path: str,
    ):

        file = Path(path)

        if not file.exists():
            return ""

        return hashlib.sha256(
            file.read_bytes()
        ).hexdigest()

    def register(
        self,
        node_name: str,
        file_path: str,
    ):

        if node_name not in self.graph.nodes:
            return

        self.graph.nodes[
            node_name
        ].prompt_hash = self.hash_file(
            file_path,
        )

        self.graph.save()

    def changed(
        self,
        node_name: str,
    ):

        if node_name not in self.graph.nodes:
            return False

        node = self.graph.nodes[node_name]

        current = self.hash_file(
            node.file_path,
        )

        return current != node.prompt_hash

    def affected_nodes(
        self,
        node_name: str,
    ):

        return self.graph.affected(
            node_name,
        )