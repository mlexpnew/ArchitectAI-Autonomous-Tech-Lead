"""
Self-Healing Loop & Retry Manager

Orchestrates the closed-loop autonomous repair cycle:
ProjectValidator -> ErrorAnalyzer -> HealingEngine -> Re-Validate -> Commit/Rollback.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from self_healing.error_analyzer import ErrorAnalyzer
from self_healing.healing_engine import HealingEngine


class SelfHealingLoop:
    """
    Autonomous closed-loop reflection & repair engine for generated backends.
    """

    def __init__(
        self,
        backend_dir: str,
        max_attempts: int = 3,
    ):
        self.backend_dir = Path(backend_dir).resolve()
        self.max_attempts = max_attempts
        self.analyzer = ErrorAnalyzer()
        self.healer = HealingEngine(backend_dir=str(self.backend_dir))

    def _create_validator(self):
        """Lazily imports ProjectValidator to prevent circular dependencies."""
        from orchestration.project_validator import ProjectValidator
        return ProjectValidator(backend_dir=str(self.backend_dir))

    def collect_failure_context(self, validation_result: Dict[str, Any]) -> str:
        """Assembles compiler errors and pytest tracebacks into a cohesive diagnostic string."""
        parts = []

        for err in validation_result.get("errors", []):
            parts.append(f"VALIDATION ERROR:\n{err}")

        test_result = validation_result.get("tests")
        if test_result:
            stdout = test_result.get("stdout", "")
            stderr = test_result.get("stderr", "")
            if stdout:
                parts.append(f"PYTEST STDOUT:\n{stdout}")
            if stderr:
                parts.append(f"PYTEST STDERR:\n{stderr}")

        return "\n\n".join(parts)

    def run(self) -> Dict[str, Any]:
        """
        Executes the autonomous self-healing loop:
        1. Validate project
        2. If green: return clean
        3. If failed: diagnose with AI reflection agent
        4. Apply atomic patch to target file
        5. Re-validate
        6. Commit if green; rollback if still broken
        """
        history: List[Dict[str, Any]] = []

        # Initial validation check
        initial_validator = self._create_validator()
        current_validation = initial_validator.validate()

        if current_validation.get("valid"):
            return {
                "healed": True,
                "clean_run": True,
                "attempts": 0,
                "validation": current_validation,
                "history": [],
                "message": "Project passed validation cleanly without requiring self-healing.",
            }

        print("\n" + "=" * 60)
        print("🛠 ENTERING AUTONOMOUS SELF-HEALING LOOP")
        print("=" * 60)

        for attempt in range(1, self.max_attempts + 1):
            print(f"\n[Attempt {attempt}/{self.max_attempts}] 🧠 Diagnosing project failure...")

            failure_context = self.collect_failure_context(current_validation)
            diagnosis_info = self.analyzer.analyze(
                failure_context=failure_context,
                backend_dir=str(self.backend_dir),
            )

            target_file = diagnosis_info.get("target_file")
            root_cause = diagnosis_info.get("root_cause")
            error_type = diagnosis_info.get("error_type")
            fix_suggestion = diagnosis_info.get("fix_suggestion")

            print(f"  • Root Cause: {root_cause}")
            print(f"  • Target File: {target_file}")
            print(f"  • Error Type: {error_type}")

            if not target_file or not (self.backend_dir / target_file).exists():
                print(f"  ⚠️ Could not resolve target file '{target_file}' inside backend.")
                history.append({
                    "attempt": attempt,
                    "target_file": target_file,
                    "root_cause": root_cause,
                    "error_type": error_type,
                    "repaired": False,
                    "error": f"Target file '{target_file}' not found in {self.backend_dir}",
                })
                continue

            # Attempt atomic repair
            print(f"  🔧 Applying atomic patch to {target_file}...")
            repair_result = self.healer.heal_file(
                relative_path=target_file,
                failure_context=failure_context,
                diagnosis=diagnosis_info.get("raw_diagnosis", root_cause),
            )

            if not repair_result.get("success"):
                print(f"  ❌ Patch application failed: {repair_result.get('error')}")
                history.append({
                    "attempt": attempt,
                    "target_file": target_file,
                    "root_cause": root_cause,
                    "error_type": error_type,
                    "repaired": False,
                    "error": repair_result.get("error"),
                })
                continue

            # Re-validate project after patch
            print("  🧪 Re-validating project with patch applied...")
            re_validator = self._create_validator()
            re_validation = re_validator.validate()

            if re_validation.get("valid"):
                # Confirmed green! Commit the repair.
                self.healer.commit(target_file)
                print(f"\n🎉 SELF-HEALING SUCCESSFUL on attempt {attempt}!")
                print(f"  ✓ {target_file} repaired and verified.")

                history.append({
                    "attempt": attempt,
                    "target_file": target_file,
                    "root_cause": root_cause,
                    "error_type": error_type,
                    "fix_suggestion": fix_suggestion,
                    "repaired": True,
                    "verified_green": True,
                })

                return {
                    "healed": True,
                    "clean_run": False,
                    "attempts": attempt,
                    "healed_file": target_file,
                    "root_cause": root_cause,
                    "validation": re_validation,
                    "history": history,
                    "message": f"Successfully self-healed {target_file} in attempt {attempt}.",
                }

            # If still invalid, rollback to prevent corruption and record attempt
            print("  ⚠️ Patch did not resolve validation errors. Rolling back...")
            self.healer.rollback(target_file)
            current_validation = re_validation
            history.append({
                "attempt": attempt,
                "target_file": target_file,
                "root_cause": root_cause,
                "error_type": error_type,
                "repaired": True,
                "verified_green": False,
                "errors_after_patch": re_validation.get("errors", []),
            })

        print("\n❌ Self-healing loop exhausted all attempts.")
        final_validator = self._create_validator()
        return {
            "healed": False,
            "clean_run": False,
            "attempts": self.max_attempts,
            "validation": final_validator.validate(),
            "history": history,
            "message": f"Self-healing exhausted {self.max_attempts} attempts without achieving 100% green tests.",
        }

    def heal(self) -> Dict[str, Any]:
        """Backward-compatible alias for run()."""
        return self.run()


class RetryManager:
    """Legacy and plugin wrapper for self-healing retries."""

    def __init__(self, retries: int = 3):
        self.retries = retries

    def execute(self, code: str, error: str) -> str:
        """Executes code healing for standalone code snippets."""
        from review.code_fixer import CodeFixer
        from validation.python_validator import PythonValidator

        fixer = CodeFixer()
        current = code
        for attempt in range(self.retries):
            fixed = fixer.fix(current, error)
            valid, msg = PythonValidator.validate(fixed)
            if valid:
                return fixed
            error = msg

        raise RuntimeError("Automatic healing failed.")


# Alias for backward compatibility
SelfHealingEngine = SelfHealingLoop