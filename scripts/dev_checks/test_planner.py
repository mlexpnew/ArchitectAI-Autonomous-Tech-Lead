from planner.task_planner import TaskPlanner
from planner.task_dispatcher import TaskDispatcher

from agents.agent_manager import AgentManager


planner = TaskPlanner()

tasks = planner.plan(

    "Hospital Management System"

)

manager = AgentManager()

TaskDispatcher(

    manager,

).dispatch(

    tasks,

)

manager.execute_all(

    "Hospital Management System",

)