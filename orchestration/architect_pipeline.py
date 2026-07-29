"""
ArchitectAI Master Pipeline

Coordinates:

Requirements
    -> AI Backend Generation
    -> Project Validation
    -> Self-Healing
    -> Autonomous Agent Workflow
    -> Artifact Collection
    -> Final Result
"""

from pathlib import Path

from agents.agent_manager import AgentManager
from generators.backend.backend_pipeline import BackendPipeline
from orchestration.project_validator import ProjectValidator
from orchestration.self_healing_engine import SelfHealingEngine
from generators.project_packaging_generator import (
    ProjectPackagingGenerator,
)
from orchestration.project_exporter import ProjectExporter


class ArchitectPipeline:
    """
    Main orchestration entry point for ArchitectAI.
    """

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)

        self.backend_pipeline = BackendPipeline(
            output_dir=str(self.output_dir),
        )

        self.agent_manager = AgentManager()

        self.blueprint = None
        self.workflow_results = None

    def generate(
        self,
        requirements: str,
        project_name: str = "Generated Project",
    ):
        """
        Execute the complete ArchitectAI pipeline.
        """

        if not requirements.strip():
            raise ValueError(
                "Project requirements cannot be empty."
            )

        print("\n" + "=" * 70)
        print("🚀 ARCHITECTAI AUTONOMOUS PIPELINE")
        print("=" * 70)

        # =================================================
        # STEP 1
        # Generate backend from natural-language requirements
        # =================================================

        print(
            "\n[1/4] 🧠 Analysing requirements "
            "and generating backend..."
        )

        self.blueprint = (
            self.backend_pipeline.generate_from_requirements(
                requirements
            )
        )

        print(
            "\n✅ Blueprint and backend generated"
        )

        backend_dir = (
            self.output_dir
            / "backend"
        )

        # =================================================
        # STEP 2
        # Validate generated project
        # =================================================

        print(
            "\n[2/4] 🔍 Validating generated backend..."
        )

        validator = ProjectValidator(
            backend_dir=str(backend_dir)
        )

        validation = validator.validate()

        healing_result = None

        # =================================================
        # SELF-HEALING
        # =================================================

        if not validation["valid"]:

            print(
                "\n⚠️ Generated backend failed validation."
            )

            print(
                "🛠 Starting ArchitectAI self-healing..."
            )

            healer = SelfHealingEngine(
                backend_dir=str(backend_dir),
                max_attempts=2,
            )

            healing_result = healer.heal()

            if not healing_result["healed"]:

                errors = (
                    healing_result
                    .get("validation", {})
                    .get("errors", [])
                )

                raise RuntimeError(
                    "ArchitectAI could not repair "
                    "the generated backend:\n"
                    + "\n".join(errors)
                )

            validation = healing_result[
                "validation"
            ]

            print(
                "\n✅ Self-healing completed successfully"
            )

        else:

            print(
                "\n✅ Backend passed validation"
            )
            
        # =================================================
        # PROJECT PACKAGING
        # =================================================

        print(
            "\n📦 Generating deployment package..."
        )

        packaging_generator = ProjectPackagingGenerator(
            output_dir=str(self.output_dir)
        )

        packaging_generator.generate(
            project_name=project_name,
            blueprint=self.blueprint,
        )

        print(
            "\n✅ Deployment package generated"
        )

        # =================================================
        # STEP 3
        # Autonomous agent workflow
        # =================================================

        print(
            "\n[3/4] 🤖 Running autonomous agents..."
        )

        self.workflow_results = (
            self.agent_manager.execute_workflow(
                project=project_name,
                workflow=[
                    "database",
                    "backend",
                    "security",
                    "qa",
                    "devops",
                    "documentation",
                ],
            )
        )

        # =================================================
        # STEP 4
        # Collect artifacts
        # =================================================

        print(
            "\n[4/4] 📦 Collecting artifacts..."
        )

        artifacts = (
            self.agent_manager.workspace.list()
        )

        # =================================================
        # FINAL PROJECT EXPORT
        # =================================================

        print(
            "\n📤 Creating final project export..."
        )

        exporter = ProjectExporter(
            output_dir=str(self.output_dir)
        )

        export_result = exporter.export(
            project_name=project_name,
            blueprint=self.blueprint,
            validation=validation,
            self_healing=healing_result,
            workflow_results=self.workflow_results,
            artifacts=artifacts,
        )

        result = {
            "project_name": project_name,
            "output_dir": str(self.output_dir),
            "blueprint": self.blueprint,
            "validation": validation,
            "self_healing": healing_result,
            "workflow_results": self.workflow_results,
            "artifacts": artifacts,
            "export": export_result,
        }

        print("\n" + "=" * 70)
        print("✅ ARCHITECTAI PIPELINE COMPLETED")
        print("=" * 70)

        return result