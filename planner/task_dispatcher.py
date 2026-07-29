"""
Task Dispatcher
"""


class TaskDispatcher:

    def __init__(
        self,
        manager,
    ):

        self.manager = manager

    def dispatch(
        self,
        tasks,
    ):

        for task in tasks:

            agent = self.manager.get(
                task.agent,
            )

            if agent:

                agent.add_task(
                    task.title,
                )