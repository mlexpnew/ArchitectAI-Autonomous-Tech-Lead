from planner.task_planner import TaskPlanner
from planner.task_executor import TaskExecutor

from agents.agent_manager import AgentManager


planner = TaskPlanner()

tasks = planner.plan(
    "Hospital Management System"
)

manager = AgentManager()

TaskExecutor(
    manager,
).execute(
    tasks,
    "Hospital Management System",
)