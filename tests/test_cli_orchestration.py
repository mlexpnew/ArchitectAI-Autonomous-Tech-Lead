"""
Tests for unified CLI, orchestrator consolidation, and review module facades.
"""

from main import build_parser, read_requirements, LEGACY_STAGES
import review
import reviewer
import orchestration
import orchestrator


def test_cli_parser_generate():
    """Verify generate subcommand argument parsing."""
    parser = build_parser()
    args = parser.parse_args([
        "generate",
        "--name", "ECommerceApp",
        "--requirements", "Build a shop",
        "--output", "outputs/custom_ecommerce",
    ])
    assert args.command == "generate"
    assert args.name == "ECommerceApp"
    assert args.requirements == "Build a shop"
    assert args.output == "outputs/custom_ecommerce"


def test_cli_parser_stage():
    """Verify stage subcommand argument parsing."""
    parser = build_parser()
    args = parser.parse_args([
        "stage", "scaffold",
        "--name", "DemoApp",
    ])
    assert args.command == "stage"
    assert args.stage_name == "scaffold"
    assert args.name == "DemoApp"


def test_legacy_stages_set():
    """Verify expected core stages are recognized."""
    assert "scaffold" in LEGACY_STAGES
    assert "generate-models" in LEGACY_STAGES
    assert "architecture" in LEGACY_STAGES
    assert "autonomous" in LEGACY_STAGES


def test_read_requirements_raw_text():
    """Ensure raw text is parsed properly."""
    raw = "Build an invoicing platform."
    assert read_requirements(raw) == raw


def test_review_namespace_consolidation():
    """Ensure review and reviewer packages expose unified classes."""
    assert hasattr(review, "CodeReviewer")
    assert hasattr(review, "CodeFixer")
    assert hasattr(review, "ReviewerAgent")
    assert hasattr(review, "ReviewManager")
    assert hasattr(review, "Review")

    assert hasattr(reviewer, "Review")
    assert hasattr(reviewer, "ReviewerAgent")
    assert hasattr(reviewer, "ReviewManager")
    assert hasattr(reviewer, "CodeReviewer")
    assert hasattr(reviewer, "CodeFixer")


def test_orchestration_namespace_consolidation():
    """Ensure orchestration and orchestrator packages cross-export unified classes."""
    assert hasattr(orchestration, "ArchitectPipeline")
    assert hasattr(orchestration, "ProjectValidator")
    assert hasattr(orchestration, "SelfHealingEngine")
    assert hasattr(orchestration, "ProjectManager")

    assert hasattr(orchestrator, "ArchitectAI")
    assert hasattr(orchestrator, "ArchitectPipeline")
    assert hasattr(orchestrator, "ProjectManager")
    assert hasattr(orchestrator, "ProgressTracker")
