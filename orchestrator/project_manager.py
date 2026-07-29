from agents.agent_manager import AgentManager

from planner.task_planner import TaskPlanner
from planner.parallel_executor import ParallelTaskExecutor

from orchestrator.progress_tracker import ProgressTracker
from techlead import decision
from techlead.tech_lead import TechLead
from planner.replanner import RePlanner
from planner.task_scheduler import TaskScheduler


class ProjectManager:

    def __init__(self):

        self.manager = AgentManager()

        self.planner = TaskPlanner()

        self.executor = ParallelTaskExecutor(self.manager)

        self.tracker = ProgressTracker()
        self.tech_lead = TechLead()
        self.replanner = RePlanner()
        self.scheduler = TaskScheduler()

    def run(self, project):

        self.tracker.start(project)

        tasks = self.planner.plan(project)

        original_run = self.executor._run_task

        def wrapped(task, project_name):

            try:

                self.tracker.running(task.agent)

                result = original_run(task, project_name)

                self.tracker.completed(task.agent)

                return result

            except Exception:

                self.tracker.failed(task.agent)

                raise

        self.executor._run_task = wrapped

        self.executor.execute(tasks, project)

        self.tracker.summary()
        decision = self.tech_lead.evaluate(
            self.tracker.state
        )

        print()

        print("========== TECH LEAD ==========")

        print(decision.message)

        print()

        print("Continue :", decision.continue_project)

        print("Retry :", decision.retry_agents)

        print("New Tasks :", decision.new_tasks)

        print("===============================")
        
        new_tasks = self.replanner.replan(
            decision
        )

        if new_tasks:

            print()

            print("Scheduling New Tasks...")

            self.scheduler.schedule(new_tasks)

            while self.scheduler.has_tasks():

                task = self.scheduler.next_task()

                print(f"Executing New Task -> {task.agent}")

                agent = self.manager.get(task.agent)

                if agent:

                    agent.add_task(task.title)

                    agent.execute(project)