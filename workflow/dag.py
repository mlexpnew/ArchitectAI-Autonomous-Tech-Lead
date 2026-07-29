"""
Workflow DAG
"""

from workflow.node import WorkflowNode


class WorkflowDAG:

    def __init__(self):

        self.nodes = {}

    def add_node(self, node: WorkflowNode):

        self.nodes[node.name] = node

    def ready_nodes(self):

        ready = []

        for node in self.nodes.values():

            if node.completed:
                continue

            if all(
                self.nodes[d].completed
                for d in node.dependencies
            ):
                ready.append(node)

        return ready

    def mark_completed(self, name: str):

        self.nodes[name].completed = True

    def finished(self):

        return all(
            node.completed
            for node in self.nodes.values()
        )