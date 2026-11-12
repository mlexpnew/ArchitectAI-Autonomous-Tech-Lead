print("TEST STARTED")

from agents.agent_manager import AgentManager

print("Creating manager...")

manager = AgentManager()

print("Executing...")

manager.execute_all(
    "Hospital Management System"
)

print("TEST FINISHED")