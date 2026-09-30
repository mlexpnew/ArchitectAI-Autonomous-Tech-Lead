"""
ArchitectAI Project Exporter

Creates:
- Generation report
- Final distributable ZIP archive
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import zipfile


class ProjectExporter:

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)
        self.backend_dir = self.output_dir / "backend"

        self.exports_dir = (
            self.output_dir / "exports"
        )

        self.exports_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _serialise_artifacts(artifacts):
        """
        Convert workspace artifacts into JSON-safe data.
        """

        result = []

        if artifacts is None:
            return result

        for artifact in artifacts:

            if isinstance(artifact, str):
                result.append(artifact)
                continue

            result.append(
                {
                    "name": getattr(
                        artifact,
                        "name",
                        str(artifact),
                    ),
                    "category": getattr(
                        artifact,
                        "category",
                        None,
                    ),
                    "author": getattr(
                        artifact,
                        "author",
                        None,
                    ),
                    "version": getattr(
                        artifact,
                        "version",
                        None,
                    ),
                }
            )

        return result

    # ---------------------------------------------------------
    # Generation Report
    # ---------------------------------------------------------

    def generate_report(
        self,
        project_name,
        blueprint,
        validation,
        self_healing,
        workflow_results,
        artifacts,
        telemetry=None,
    ):
        entities = []

        for entity in blueprint.entities:

            fields = []

            for field in entity.fields:

                fields.append(
                    {
                        "name": field.name,
                        "type": field.type,
                    }
                )

            entities.append(
                {
                    "name": entity.name,
                    "fields": fields,
                }
            )

        relationships = []

        for relation in blueprint.relationships:

            relationships.append(
                {
                    "source": relation.source,
                    "target": relation.target,
                    "type": relation.relationship_type,
                    "foreign_key": relation.foreign_key,
                }
            )

        healing_summary = {
            "required": self_healing is not None,
            "healed": (
                self_healing.get("healed")
                if isinstance(self_healing, dict)
                else None
            ),
            "attempts": (
                self_healing.get("attempts")
                if isinstance(self_healing, dict)
                else 0
            ),
        }

        test_summary = {
            "passed": None,
            "failed": None,
            "warnings": None,
        }

        tests = validation.get("tests")

        if tests:

            stdout = tests.get(
                "stdout",
                "",
            )

            import re

            passed = re.search(
                r"(\d+)\s+passed",
                stdout,
            )

            failed = re.search(
                r"(\d+)\s+failed",
                stdout,
            )

            warnings = re.search(
                r"(\d+)\s+warning",
                stdout,
            )

            test_summary["passed"] = (
                int(passed.group(1))
                if passed
                else 0
            )

            test_summary["failed"] = (
                int(failed.group(1))
                if failed
                else 0
            )

            test_summary["warnings"] = (
                int(warnings.group(1))
                if warnings
                else 0
            )
            
            statistics = self.generate_statistics(
                    blueprint
                    )
            
            
            metrics = {
            "lines_of_code": self.count_lines_of_code(),
            "python_files": statistics["python_files"],
            "total_files": statistics["total_files"],
            "entities_generated": statistics["entities"],
            "relationships_generated": statistics["relationships"],
            "models_generated": statistics["models"],
            "schemas_generated": statistics["schemas"],
            "repositories_generated": statistics["repositories"],
            "services_generated": statistics["services"],
            "apis_generated": statistics["apis"],
            "validation_status": (
                "passed"
                if validation.get("valid")
                else "failed"
            ),
            "tests_passed": test_summary["passed"],
            "tests_failed": test_summary["failed"],
        }

        report = {
            "generator": "ArchitectAI Autonomous Tech Lead",
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "project_name": project_name,

            "statistics": statistics,
            "metrics": metrics,
            "entities": entities,
            "relationships": relationships,
            "validation": validation,
            "test_summary": test_summary,
            "self_healing": healing_summary,
            "workflow_results": (
                workflow_results
                if isinstance(
                    workflow_results,
                    (dict, list, str, int, float, bool)
                )
                or workflow_results is None
                else str(workflow_results)
            ),
            "artifacts": self._serialise_artifacts(
                artifacts
            ),
            "telemetry": telemetry or {},
            "statistics": statistics,
        }

        report_path = (
            self.exports_dir
            / "generation_report.json"
        )

        report_path.write_text(
            json.dumps(
                report,
                indent=4,
                default=str,
            ),
            encoding="utf-8",
        )

        print(
            f"✅ Generation report: {report_path}"
        )
        
        

        return report_path

    def generate_blueprint(
        self,
        project_name,
        blueprint,
    ):
        entities = []

        for entity in blueprint.entities:
            fields = []

            for field in entity.fields:
                fields.append(
                    {
                        "name": field.name,
                        "type": field.type,
                    }
                )

            entities.append(
                {
                    "name": entity.name,
                    "fields": fields,
                }
            )

        relationships = []

        for relation in blueprint.relationships:
            relationships.append(
                {
                    "source": relation.source,
                    "target": relation.target,
                    "type": relation.relationship_type,
                    "foreign_key": relation.foreign_key,
                }
            )

        blueprint_json = {
            "project_name": project_name,
            "backend": "FastAPI",
            "database": "SQLite",
            "entities": entities,
            "relationships": relationships,
        }

        blueprint_path = (
            self.exports_dir
            / "project_blueprint.json"
        )

        blueprint_path.write_text(
            json.dumps(
                blueprint_json,
                indent=4,
            ),
            encoding="utf-8",
        )

        print(
            f"✅ Project blueprint: {blueprint_path}"
        )

        return blueprint_path

    # ---------------------------------------------------------
    # ZIP Export
    # ---------------------------------------------------------

    def create_archive(
            self,
            project_name: str,
        ):
            safe_name = (
                project_name
                .strip()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            archive_path = (
                self.exports_dir
                / f"{safe_name}.zip"
            )

            excluded_dirs = {
                "__pycache__",
                ".pytest_cache",
                ".git",
            }

            excluded_files = {
                "app.db",
            }

            excluded_extensions = {
                ".pyc",
                ".bak",
            }

            with zipfile.ZipFile(
                archive_path,
                "w",
                zipfile.ZIP_DEFLATED,
            ) as zipf:

                for path in self.backend_dir.rglob("*"):

            # Skip excluded directories
                    if any(
                        part in excluded_dirs
                        for part in path.parts
                    ):
                        continue

            # Skip unwanted files
                    if path.is_file():

                        if path.name in excluded_files:
                            continue

                        if path.suffix in excluded_extensions:
                            continue

                        zipf.write(
                            path,
                            arcname=path.relative_to(
                                self.backend_dir
                            ),
                        )

            print(
                f"✅ Project archive: {archive_path}"
            )

            return archive_path
    # ---------------------------------------------------------
    # Export Pipeline
    # ---------------------------------------------------------

    def export(
        self,
        project_name,
        blueprint,
        validation,
        self_healing,
        workflow_results,
        artifacts,
        telemetry=None,
    ):
        print("\n" + "=" * 60)
        print("📤 Exporting Generated Project")
        print("=" * 60)

        if not self.backend_dir.exists():
            raise FileNotFoundError(
                f"Backend directory does not exist: "
                f"{self.backend_dir}"
            )

        report_path = self.generate_report(
            project_name=project_name,
            blueprint=blueprint,
            validation=validation,
            self_healing=self_healing,
            workflow_results=workflow_results,
            artifacts=artifacts,
            telemetry=telemetry,
        )
        
        blueprint_path = self.generate_blueprint(
            project_name=project_name,
            blueprint=blueprint,
        )

        archive_path = self.create_archive(
            project_name=project_name
        )

        print(
            "\n✅ Project export completed"
        )

        return {
            "report": str(report_path),
            "archive": str(archive_path),
            "blueprint": str(blueprint_path),
        }
        
    # ---------------------------------------------------------
    # Project Statistics
    # ---------------------------------------------------------

    def generate_statistics(
        self,
        blueprint,
    ):
        python_files = list(
            self.backend_dir.rglob("*.py")
        )

        all_files = [
            f
            for f in self.backend_dir.rglob("*")
            if f.is_file()
        ]

        return {
            "entities": len(blueprint.entities),
            "relationships": len(blueprint.relationships),
            "models": len(
                list(
                    (self.backend_dir / "app/models").glob("*.py")
                )
            ) - 1,   # exclude __init__.py

            "schemas": len(
                list(
                    (self.backend_dir / "app/schemas").glob("*.py")
                )
            ) - 1,

            "repositories": len(
                list(
                    (self.backend_dir / "app/repositories").glob("*.py")
                )
            ) - 1,

            "services": len(
                list(
                    (self.backend_dir / "app/services").glob("*.py")
                )
            ) - 1,

            "apis": len(
                list(
                    (self.backend_dir / "app/api").glob("*.py")
                )
            ) - 1,

            "python_files": len(python_files),
            "total_files": len(all_files),
        }
        
    def count_lines_of_code(self):
        total = 0

        for file in self.backend_dir.rglob("*.py"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                        otal += sum(1 for _ in f)
            except Exception:
                pass

        return total
