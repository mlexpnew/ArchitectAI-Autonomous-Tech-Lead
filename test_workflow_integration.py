from agents.agent_manager import AgentManager


manager = AgentManager()

print("\nRegistered agents:")
print(manager.list_agents())

results = manager.execute_workflow(
    project="Hospital Management System",
    workflow=[
        "database",
        "backend",
        "qa",
        "documentation",
    ],
)

print("\nWorkflow results:")
print(results)

print("\nPublished artifacts:")

for artifact in manager.workspace.list():
    print(
        artifact.name,
        artifact.category,
        artifact.author,
        f"v{artifact.version}",
    )

print("\n✅ WORKFLOW INTEGRATION SUCCESSFUL")
