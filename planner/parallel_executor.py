"""
Parallel Task Executor
"""

from concurrent.futures import ThreadPoolExecutor

from planner.task_graph import TaskGraph
from planner.task_dispatcher import TaskDispatcher


class ParallelTaskExecutor:

    def __init__(self, manager):

        self.manager = manager
        self.dispatcher = TaskDispatcher(manager)

    def _run_task(self, task, project):

        print(f"Running {task.agent}")

        self.dispatcher.dispatch([task])

        agent = self.manager.get(task.agent)

        if agent:
            agent.execute(project)

        return task.agent

    def execute(self, tasks, project):

        graph = TaskGraph()

        completed = set()

        for task in tasks:
            graph.add(task)

        while len(completed) < len(tasks):

            ready = graph.ready(completed)

            if not ready:
                raise RuntimeError("Circular dependency detected.")

            with ThreadPoolExecutor(max_workers=len(ready)) as executor:

                futures = [
                    executor.submit(
                        self._run_task,
                        task,
                        project,
                    )
                    for task in ready
                ]

                for future in futures:
                    completed.add(future.result())