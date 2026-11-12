from planner.task_planner import TaskPlanner
from planner.parallel_executor import ParallelTaskExecutor

from agents.agent_manager import AgentManager


planner = TaskPlanner()

tasks = planner.plan(
    "Hospital Management System"
)

manager = AgentManager()

ParallelTaskExecutor(
    manager,
).execute(
    tasks,
    "Hospital Management System",
)