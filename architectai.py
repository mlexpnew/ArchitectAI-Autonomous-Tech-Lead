"""
ArchitectAI Command Line Interface

Generate production-ready backend projects
from natural-language requirements.
"""

import argparse
import sys
from pathlib import Path

from orchestration.architect_pipeline import ArchitectPipeline


def read_requirements(path: str) -> str:
    requirements_path = Path(path)

    if not requirements_path.exists():
        raise FileNotFoundError(
            f"Requirements file not found: {path}"
        )

    content = requirements_path.read_text(
        encoding="utf-8"
    ).strip()

    if not content:
        raise ValueError(
            "Requirements file is empty."
        )

    return content


def generate_project(args):
    print("\n" + "=" * 70)
    print("🏗 ARCHITECTAI PROJECT GENERATOR")
    print("=" * 70)

    requirements = read_requirements(
        args.requirements
    )

    pipeline = ArchitectPipeline(
        output_dir=args.output
    )

    result = pipeline.generate(
        requirements=requirements,
        project_name=args.name,
    )

    print("\n" + "=" * 70)
    print("🎉 PROJECT GENERATED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"\nProject: {result['project_name']}"
    )

    print(
        f"Output: {result['output_dir']}"
    )

    validation = result.get(
        "validation",
        {}
    )

    print(
        f"Validation: "
        f"{'PASSED' if validation.get('valid') else 'FAILED'}"
    )

    tests = validation.get(
        "tests",
        {}
    )

    if tests:
        print(
            f"Tests: "
            f"{'PASSED' if tests.get('passed') else 'FAILED'}"
        )

    export_result = result.get(
        "export",
        {}
    )

    if export_result:
        print(
            f"\nReport: {export_result.get('report')}"
        )

        print(
            f"Archive: {export_result.get('archive')}"
        )

    print(
        "\n🚀 ArchitectAI generation complete."
    )

    return result


def build_parser():
    parser = argparse.ArgumentParser(
        prog="architectai",
        description=(
            "ArchitectAI Autonomous Tech Lead - "
            "Generate software from natural-language "
            "requirements."
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a new software project",
    )

    generate_parser.add_argument(
        "--name",
        required=True,
        help="Project name",
    )

    generate_parser.add_argument(
        "--requirements",
        required=True,
        help="Path to requirements text file",
    )

    generate_parser.add_argument(
        "--output",
        required=True,
        help="Generated project output directory",
    )

    generate_parser.set_defaults(
        func=generate_project
    )

    return parser


def main():
    parser = build_parser()

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    try:
        args.func(args)
        return 0

    except KeyboardInterrupt:
        print(
            "\n⚠️ Generation cancelled."
        )
        return 130

    except Exception as exc:
            import traceback

            print("\n========== FULL ERROR ==========\n")
            traceback.print_exc()

            print(
                f"\n❌ ArchitectAI failed: {exc}",
                file=sys.stderr,
            )

            return 1


if __name__ == "__main__":
    raise SystemExit(main())