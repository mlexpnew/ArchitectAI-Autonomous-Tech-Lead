from agents.agent_manager import AgentManager

print("TEST STARTED")

manager = AgentManager()

manager.get("backend").add_task("Generate FastAPI Backend")
manager.get("database").add_task("Generate SQLAlchemy Models")
manager.get("qa").add_task("Generate Pytest Tests")
manager.get("documentation").add_task("Generate README.md")

manager.execute_all("Hospital Management System")

print("TEST FINISHED")
