"""
Agent orchestration tests.
"""

from agents.agent_manager import AgentManager


def test_agent_manager_initialization():
    manager = AgentManager()

    expected_agents = {
        "backend",
        "frontend",
        "database",
        "devops",
        "qa",
        "security",
        "documentation",
    }

    assert set(manager.agents.keys()) == expected_agents


def test_agent_task_assignment():
    manager = AgentManager()

    backend = manager.get("backend")

    backend.add_task("Generate FastAPI Backend")

    assert backend.has_tasks()
    assert "Generate FastAPI Backend" in backend.get_tasks()


def test_agent_orchestration():
    manager = AgentManager()

    manager.get("backend").add_task(
        "Generate FastAPI Backend"
    )

    manager.get("database").add_task(
        "Generate SQLAlchemy Models"
    )

    manager.get("qa").add_task(
        "Generate Pytest Tests"
    )

    manager.get("documentation").add_task(
        "Generate README.md"
    )

    manager.execute_all(
        "Hospital Management System"
    )

    artifacts = manager.workspace.list()

    assert len(artifacts) > 0


def test_workspace_artifacts():
    manager = AgentManager()

    backend = manager.get("backend")

    backend.add_task(
        "Generate FastAPI Backend"
    )

    backend.execute(
        "Hospital Management System"
    )

    artifacts = manager.workspace.list()

    assert len(artifacts) >= 1

    artifact = artifacts[0]

    assert artifact.name
    assert artifact.category
    assert artifact.author
    assert artifact.content is not None
