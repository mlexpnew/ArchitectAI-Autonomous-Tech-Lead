"""
Task Dependency Graph
"""


class TaskGraph:

    def __init__(self):

        self.tasks = {}

    def add(self, task):

        self.tasks[task.agent] = task

    def ready(self, completed):

        ready = []

        for task in self.tasks.values():

            if task.agent in completed:
                continue

            if all(dep in completed for dep in task.depends_on):

                ready.append(task)

        return ready