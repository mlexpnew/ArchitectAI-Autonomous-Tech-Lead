from collections import deque


class TaskQueue:

    def __init__(self):

        self.queue = deque()

    def add(self, task):

        self.queue.append(task)

    def extend(self, tasks):

        self.queue.extend(tasks)

    def pop(self):

        if self.queue:

            return self.queue.popleft()

        return None

    def empty(self):

        return len(self.queue) == 0

    def __len__(self):

        return len(self.queue)