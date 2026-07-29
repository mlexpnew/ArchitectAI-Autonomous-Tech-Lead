from planner.task import ProjectTask


class RePlanner:

    def replan(self, decision):

        tasks = []

        for item in decision.new_tasks:

            tasks.append(

                ProjectTask(

                    agent=item["agent"],

                    title=item["title"],

                    description=item["description"],

                    priority=item.get("priority", 1),

                    depends_on=item.get("depends_on", [])

                )

            )

        return tasks