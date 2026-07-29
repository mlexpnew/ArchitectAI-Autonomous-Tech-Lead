"""
Dependency Executor
"""

from planner.task_dispatcher import TaskDispatcher
from planner.task_graph import TaskGraph


class TaskExecutor:

    def __init__(

        self,

        manager,

    ):

        self.manager = manager

        self.dispatcher = TaskDispatcher(manager)

    def execute(

        self,

        tasks,

        project,

    ):

        graph = TaskGraph()

        completed = set()

        for task in tasks:

            graph.add(task)

        while len(completed) < len(tasks):

            ready = graph.ready(completed)

            if not ready:

                raise RuntimeError(
                    "Circular dependency detected."
                )

            for task in ready:

                print(f"Executing {task.agent}")

                self.dispatcher.dispatch([task])

                self.manager.get(task.agent).execute(project)

                completed.add(task.agent)