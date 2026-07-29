from planner.task_queue import TaskQueue


class TaskScheduler:

    def __init__(self):

        self.queue = TaskQueue()

    def schedule(self, tasks):

        tasks = sorted(
            tasks,
            key=lambda x: x.priority,
            reverse=True,
        )

        self.queue.extend(tasks)

    def next_task(self):

        return self.queue.pop()

    def has_tasks(self):

        return not self.queue.empty()