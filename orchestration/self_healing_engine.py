"""
ArchitectAI Self-Healing Engine

Automatically validates generated projects,
diagnoses failures, repairs generated Python files,
revalidates the project, and rolls back failed repairs.
"""

from pathlib import Path
import re
import shutil

from generators.ai.code_generator import AICodeGenerator
from orchestration.project_validator import ProjectValidator
from orchestration.code_repair_engine import CodeRepairEngine


class SelfHealingEngine:

    def __init__(
        self,
        backend_dir: str,
        max_attempts: int = 2,
    ):
        self.backend_dir = Path(
            backend_dir
        ).resolve()

        self.max_attempts = max_attempts

        self.ai = AICodeGenerator()

        self.repair_engine = CodeRepairEngine(
            backend_dir=str(self.backend_dir)
        )

    # ---------------------------------------------------------
    # Failure Context
    # ---------------------------------------------------------

    def collect_failure_context(
        self,
        validation_result: dict,
    ):
        """
        Collect validator and pytest failures.
        """

        parts = []

        for error in validation_result.get(
            "errors",
            [],
        ):
            parts.append(
                f"VALIDATION ERROR:\n{error}"
            )

        test_result = validation_result.get(
            "tests"
        )

        if test_result:

            stdout = test_result.get(
                "stdout",
                ""
            )

            stderr = test_result.get(
                "stderr",
                ""
            )

            if stdout:
                parts.append(
                    f"PYTEST STDOUT:\n{stdout}"
                )

            if stderr:
                parts.append(
                    f"PYTEST STDERR:\n{stderr}"
                )

        return "\n\n".join(parts)

    # ---------------------------------------------------------
    # AI Diagnosis
    # ---------------------------------------------------------

    def diagnose(
        self,
        validation_result: dict,
    ):
        """
        Diagnose project failure.
        """

        context = self.collect_failure_context(
            validation_result
        )

        prompt = f"""
You are a senior Python, FastAPI and SQLAlchemy engineer.

An automatically generated backend failed validation.

Analyse the error.

Return a concise technical diagnosis containing:

ROOT_CAUSE:
<root cause>

FILE:
<relative Python file path>

FIX:
<exact technical fix>

Rules:

- FILE must be relative to the backend directory.
- FILE must point to an existing Python file.
- Do not use Markdown.
- Do not use code fences.
- Do not suggest unrelated changes.

Backend directory:

{self.backend_dir}

Failure information:

{context}
"""

        return self.ai.generate(
            prompt
        )

    # ---------------------------------------------------------
    # Extract Repair Target
    # ---------------------------------------------------------

    def extract_file(
        self,
        diagnosis: str,
    ):
        """
        Extract FILE from structured AI diagnosis.
        """

        match = re.search(
            r"FILE:\s*(.+?\.py)",
            diagnosis,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        relative_path = (
            match.group(1)
            .strip()
            .strip("`")
            .strip()
        )

        return relative_path

    # ---------------------------------------------------------
    # Rollback
    # ---------------------------------------------------------

    def rollback(
        self,
        relative_path: str,
    ):
        """
        Restore the backup created by CodeRepairEngine.
        """

        target = (
            self.backend_dir
            / relative_path
        ).resolve()

        backup = target.with_suffix(
            target.suffix + ".bak"
        )

        if not backup.exists():

            print(
                f"⚠️ No backup found for "
                f"{relative_path}"
            )

            return False

        shutil.copy2(
            backup,
            target,
        )

        print(
            f"↩️ Rolled back: {relative_path}"
        )

        return True

    # ---------------------------------------------------------
    # Self-Healing Loop
    # ---------------------------------------------------------

    def heal(self):
        """
        Validate → diagnose → repair → revalidate.

        Failed repairs are rolled back automatically.
        """

        history = []

        for attempt in range(
            1,
            self.max_attempts + 1,
        ):

            print(
                "\n" + "=" * 60
            )

            print(
                f"🛠 Self-Healing Attempt "
                f"{attempt}/{self.max_attempts}"
            )

            print(
                "=" * 60
            )

            # ---------------------------------------------
            # Validate current project
            # ---------------------------------------------

            validator = ProjectValidator(
                backend_dir=str(
                    self.backend_dir
                )
            )

            validation = (
                validator.validate()
            )

            # ---------------------------------------------
            # Already healthy
            # ---------------------------------------------

            if validation["valid"]:

                print(
                    "\n✅ Project is healthy."
                )

                return {
                    "healed": True,
                    "attempts": attempt - 1,
                    "validation": validation,
                    "history": history,
                }

            # ---------------------------------------------
            # Collect failure
            # ---------------------------------------------

            failure_context = (
                self.collect_failure_context(
                    validation
                )
            )

            print(
                "\n🧠 Diagnosing failure..."
            )

            diagnosis = self.diagnose(
                validation
            )

            print(
                "\n========== AI DIAGNOSIS =========="
            )

            print(diagnosis)

            print(
                "=================================="
            )

            # ---------------------------------------------
            # Determine broken file
            # ---------------------------------------------

            repair_file = self.extract_file(
                diagnosis
            )

            if not repair_file:

                print(
                    "\n❌ Could not determine "
                    "repair target."
                )

                history.append(
                    {
                        "attempt": attempt,
                        "diagnosis": diagnosis,
                        "file": None,
                        "repaired": False,
                    }
                )

                break

            print(
                f"\n🎯 Repair target: "
                f"{repair_file}"
            )

            # ---------------------------------------------
            # Controlled repair
            # ---------------------------------------------

            try:

                repair_result = (
                    self.repair_engine.repair_file(
                        relative_path=repair_file,
                        failure_context=failure_context,
                        diagnosis=diagnosis,
                    )
                )

            except Exception as exc:

                print(
                    f"\n❌ Repair failed: {exc}"
                )

                history.append(
                    {
                        "attempt": attempt,
                        "diagnosis": diagnosis,
                        "file": repair_file,
                        "repaired": False,
                        "error": str(exc),
                    }
                )

                continue

            # ---------------------------------------------
            # Revalidate repaired project
            # ---------------------------------------------

            print(
                "\n🔄 Revalidating repaired project..."
            )

            new_validator = ProjectValidator(
                backend_dir=str(
                    self.backend_dir
                )
            )

            new_validation = (
                new_validator.validate()
            )

            # ---------------------------------------------
            # Evaluate repair success
            # ---------------------------------------------

            if new_validation.get("valid"):
                self.repair_engine.commit(
                    repair_file
                )

                history.append(
                    {
                        "attempt": attempt,
                        "diagnosis": diagnosis,
                        "file": repair_file,
                        "repaired": True,
                        "validation_passed": True,
                    }
                )

                print(
                    "\n🎉 SELF-HEALING SUCCESSFUL"
                )

                return {
                    "healed": True,
                    "attempts": attempt,
                    "validation": new_validation,
                    "history": history,
                }
            else:
                # ---------------------------------------------
                # Repair failed → rollback
                # ---------------------------------------------

                print(
                    "\n⚠️ Repair did not solve "
                    "the failure."
                )

                self.repair_engine.rollback(
                    repair_file
                )

                history.append(
                    {
                        "attempt": attempt,
                        "diagnosis": diagnosis,
                        "file": repair_file,
                        "repaired": True,
                        "validation_passed": False,
                        "repair_result": repair_result,
                    }
                )

        # -------------------------------------------------
        # Exhausted repair attempts
        # -------------------------------------------------

        print(
            "\n❌ Self-healing attempts exhausted."
        )

        final_validator = ProjectValidator(
            backend_dir=str(
                self.backend_dir
            )
        )

        final_validation = (
            final_validator.validate()
        )

        return {
            "healed": False,
            "attempts": self.max_attempts,
            "validation": final_validation,
            "history": history,
        }