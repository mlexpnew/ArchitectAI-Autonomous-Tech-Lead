"""
ArchitectAI Universal CLI Entry Point

Unified command-line interface supporting end-to-end autonomous generation,
single-stage execution, and multi-agent workflows.
"""

import argparse
from pathlib import Path
import sys

from autonomous.tech_lead import AutonomousTechLead
from builder.project_builder import AIProjectBuilder
from crews.engineering_crew import EngineeringCrew
from generators.api_generator import APIGenerator
from generators.backend_generator import BackendGenerator
from generators.master_generator import MasterGenerator
from generators.model_generator import ModelGenerator
from generators.repository_generator import RepositoryGenerator
from generators.schema_generator import SchemaGenerator
from generators.service_generator import ServiceGenerator
from orchestration.architect_pipeline import ArchitectPipeline
from orchestrator import ArchitectAI
from utils.project_scaffolder import ProjectScaffolder

DEFAULT_PROJECT_NAME = "Hospital_Management_System"
DEFAULT_REQUIREMENTS = """
Build an AI-powered Hospital Management System.

The system should allow patients to book appointments,
consult doctors online, manage prescriptions,
make payments, and allow hospital staff to manage
patients, doctors, billing, reports and inventory.
""".strip()

LEGACY_STAGES = {
    "scaffold",
    "generate-models",
    "generate-schemas",
    "generate-repositories",
    "generate-services",
    "generate-api",
    "generate-backend",
    "generate-project",
    "ai",
    "build",
    "autonomous",
    "requirement",
    "architecture",
    "backend",
    "database",
    "frontend",
}


def read_requirements(path_or_text: str) -> str:
    """Reads requirements from a file path if it exists, otherwise treats as raw text."""
    p = Path(path_or_text)
    if p.exists() and p.is_file():
        content = p.read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError(f"Requirements file '{path_or_text}' is empty.")
        return content
    if not path_or_text.strip():
        raise ValueError("Requirements cannot be empty.")
    return path_or_text.strip()


def run_pipeline(project_name: str, requirements: str, output_dir: str):
    """Executes the master ArchitectPipeline."""
    req_content = read_requirements(requirements)
    pipeline = ArchitectPipeline(output_dir=output_dir)
    return pipeline.generate(requirements=req_content, project_name=project_name)


def run_stage(stage: str, project_name: str, requirements: str, output_dir: str):
    """Executes a specific generation or engineering stage."""
    stage = stage.lower().strip()
    req_content = read_requirements(requirements)

    if stage == "scaffold":
        scaffolder = ProjectScaffolder(output_dir=output_dir)
        scaffolder.create()
        print(f"\n✅ Project folder structure created successfully at: {output_dir}")
        return

    if stage == "generate-models":
        ModelGenerator(output_dir=output_dir).generate()
        return

    if stage == "generate-schemas":
        SchemaGenerator(output_dir=output_dir).generate()
        return

    if stage == "generate-repositories":
        RepositoryGenerator(output_dir=output_dir).generate()
        return

    if stage == "generate-services":
        ServiceGenerator(output_dir=output_dir).generate()
        return

    if stage == "generate-api":
        APIGenerator(output_dir=output_dir).generate()
        return

    if stage == "generate-backend":
        BackendGenerator(output_dir=output_dir, project_name=project_name).generate()
        return

    if stage == "generate-project":
        MasterGenerator(output_dir=output_dir, project_name=project_name).generate()
        return

    if stage == "ai":
        ArchitectAI(output_dir=output_dir).build(req_content)
        return

    if stage == "build":
        AIProjectBuilder(output_dir).build(req_content)
        return

    if stage == "autonomous":
        AutonomousTechLead(output_dir).build(req_content)
        return

    if stage in {"requirement", "architecture", "backend", "database", "frontend"}:
        crew = EngineeringCrew(project_name=project_name, project_idea=req_content)
        crew.run(stage)
        return

    raise ValueError(f"Unknown stage: '{stage}'. Allowed stages: {sorted(LEGACY_STAGES)}")


def build_parser() -> argparse.ArgumentParser:
    """Builds unified CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="ArchitectAI Autonomous Tech Lead - Unified Software Generator",
    )

    subparsers = parser.add_subparsers(dest="command")

    # generate subcommand (Master Pipeline)
    gen_parser = subparsers.add_parser(
        "generate",
        help="Execute master autonomous generation pipeline",
    )
    gen_parser.add_argument(
        "--name",
        default=DEFAULT_PROJECT_NAME,
        help=f"Project name (default: {DEFAULT_PROJECT_NAME})",
    )
    gen_parser.add_argument(
        "--requirements",
        default=DEFAULT_REQUIREMENTS,
        help="Path to requirements file or raw requirements text",
    )
    gen_parser.add_argument(
        "--output",
        default=None,
        help="Target output directory (default: outputs/<name>)",
    )

    # stage subcommand
    stage_parser = subparsers.add_parser(
        "stage",
        help="Execute a specific generation or engineering stage",
    )
    stage_parser.add_argument(
        "stage_name",
        choices=sorted(LEGACY_STAGES),
        help="Name of the stage to execute",
    )
    stage_parser.add_argument(
        "--name",
        default=DEFAULT_PROJECT_NAME,
        help=f"Project name (default: {DEFAULT_PROJECT_NAME})",
    )
    stage_parser.add_argument(
        "--requirements",
        default=DEFAULT_REQUIREMENTS,
        help="Path to requirements file or raw requirements text",
    )
    stage_parser.add_argument(
        "--output",
        default=None,
        help="Target output directory",
    )

    return parser


def main():
    # Backwards compatibility: handle "python3 main.py <stage_name>" directly
    if len(sys.argv) >= 2 and sys.argv[1].lower() in LEGACY_STAGES:
        stage = sys.argv[1].lower()
        project_name = DEFAULT_PROJECT_NAME
        requirements = DEFAULT_REQUIREMENTS
        output_dir = f"outputs/{project_name}"

        # Parse any optional flags passed after the stage
        rem = sys.argv[2:]
        if "--name" in rem:
            idx = rem.index("--name")
            if idx + 1 < len(rem):
                project_name = rem[idx + 1]
                output_dir = f"outputs/{project_name}"
        if "--requirements" in rem:
            idx = rem.index("--requirements")
            if idx + 1 < len(rem):
                requirements = rem[idx + 1]
        if "--output" in rem:
            idx = rem.index("--output")
            if idx + 1 < len(rem):
                output_dir = rem[idx + 1]

        run_stage(stage, project_name, requirements, output_dir)
        return

    parser = build_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        print("\nAvailable stages for quick execution (e.g., 'python3 main.py scaffold'):")
        for s in sorted(LEGACY_STAGES):
            print(f"  python3 main.py {s}")
        return

    args = parser.parse_args()

    if args.command == "generate":
        output_dir = args.output or f"outputs/{args.name}"
        run_pipeline(args.name, args.requirements, output_dir)
        return

    if args.command == "stage":
        output_dir = args.output or f"outputs/{args.name}"
        run_stage(args.stage_name, args.name, args.requirements, output_dir)
        return

    parser.print_help()


if __name__ == "__main__":
    main()