"""
Tests for System Design Workflow Reference, templates, documentation,
and the Solution Architect agent & task integration.
"""

from pathlib import Path

from agents.solution_architect import create_solution_architect
from tasks.architecture_tasks import create_architecture_task


def test_solution_architect_agent():
    """Verify that Solution Architect agent is initialized with proper role and goal."""
    architect = create_solution_architect()
    assert architect.role == "Principal Solution Architect"
    assert "System Design Workflow" in architect.goal


def test_architecture_task_creation():
    """Verify that Architecture Task incorporates the 15-step workflow guidelines."""
    architect = create_solution_architect()
    sample_reqs = "Build a global ride-sharing platform with high availability."
    task = create_architecture_task(architect, sample_reqs)

    assert task.agent == architect
    assert "System Design Workflow" in task.description
    assert "Mermaid Architecture Diagram" in task.description
    assert "Reliability & Resilience" in task.description
    assert "Trade-off Analysis" in task.description


def test_templates_exist_and_non_empty():
    """Ensure all architecture and engineering templates are populated."""
    template_dir = Path("templates")
    expected_templates = [
        "architecture_template.md",
        "brd_template.md",
        "api_template.md",
        "sprint_template.md",
    ]

    for filename in expected_templates:
        file_path = template_dir / filename
        assert file_path.exists(), f"Missing template: {filename}"
        assert file_path.stat().st_size > 100, f"Template {filename} is empty or too short."


def test_docs_exist_and_non_empty():
    """Ensure all workflow and architecture documentation files are populated."""
    docs_dir = Path("docs")
    expected_docs = [
        "workflow.md",
        "architecture.md",
        "api.md",
    ]

    for filename in expected_docs:
        file_path = docs_dir / filename
        assert file_path.exists(), f"Missing doc: {filename}"
        assert file_path.stat().st_size > 100, f"Doc {filename} is empty or too short."
