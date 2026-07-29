"""
Workflow Engine Tests
"""

from agents.agent_manager import AgentManager
from orchestration.workflow_engine import WorkflowEngine


def test_workflow_engine_initialization():

    manager = AgentManager()

    workflow = WorkflowEngine(
        manager
    )

    assert workflow.agent_manager is manager


def test_default_workflow_agents_exist():

    manager = AgentManager()

    workflow = WorkflowEngine(
        manager
    )

    for agent_name in workflow.DEFAULT_WORKFLOW:

        assert manager.get(agent_name) is not None


def test_workflow_execution():

    manager = AgentManager()

    workflow = WorkflowEngine(
        manager
    )

    results = workflow.execute(
        "Hospital Management System"
    )

    assert isinstance(
        results,
        dict,
    )

    assert set(results.keys()) == set(
        workflow.DEFAULT_WORKFLOW
    )