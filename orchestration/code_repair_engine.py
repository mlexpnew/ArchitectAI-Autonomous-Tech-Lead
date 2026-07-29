"""
ArchitectAI Controlled Code Repair Engine

Safely repairs existing generated Python source files.

Security rules:
- Repair must remain inside generated backend.
- Only existing Python files may be repaired.
- Tests cannot be modified automatically.
- Cache/internal files cannot be modified.
- Candidate repair must compile before acceptance.
- Original source is always backed up first.
"""

from pathlib import Path
import py_compile
import shutil

from generators.ai.code_generator import AICodeGenerator


class CodeRepairEngine:

    ALLOWED_DIRECTORIES = {
        "app",
    }

    BLOCKED_DIRECTORIES = {
        "tests",
        "__pycache__",
        ".pytest_cache",
        ".venv",
        "venv",
    }

    def __init__(
        self,
        backend_dir: str,
    ):
        self.backend_dir = Path(
            backend_dir
        ).resolve()

        self.ai = AICodeGenerator()

    # ---------------------------------------------------------
    # Safe Path Resolution
    # ---------------------------------------------------------

    def _resolve_safe_file(
        self,
        relative_path: str,
    ):
        """
        Resolve and validate an AI-proposed repair target.
        """

        if not relative_path:
            raise ValueError(
                "Repair target cannot be empty."
            )

        supplied_path = Path(
            relative_path
        )

        if supplied_path.is_absolute():
            raise ValueError(
                "Repair target must be relative "
                "to the backend directory."
            )

        target = (
            self.backend_dir
            / supplied_path
        ).resolve()

        # Ensure path remains inside backend.
        try:

            relative_target = target.relative_to(
                self.backend_dir
            )

        except ValueError as exc:

            raise ValueError(
                "Repair target is outside "
                "the generated backend."
            ) from exc

        # Python only.
        if target.suffix.lower() != ".py":

            raise ValueError(
                "Automatic repair is restricted "
                "to Python files."
            )

        # Existing files only.
        if not target.exists():

            raise FileNotFoundError(
                f"Repair target does not exist: "
                f"{relative_path}"
            )

        if not target.is_file():

            raise ValueError(
                "Repair target must be a file."
            )

        parts = set(
            relative_target.parts
        )

        # Never let AI repair tests or environment/cache files.
        if parts.intersection(
            self.BLOCKED_DIRECTORIES
        ):

            raise ValueError(
                "Automatic repair is not allowed "
                f"for this path: {relative_path}"
            )

        # Restrict repairs to app/.
        if (
            not relative_target.parts
            or relative_target.parts[0]
            not in self.ALLOWED_DIRECTORIES
        ):

            raise ValueError(
                "Automatic repair is restricted "
                "to generated app source files."
            )

        return target

    # ---------------------------------------------------------
    # Backup
    # ---------------------------------------------------------

    @staticmethod
    def _backup_path(
        target: Path,
    ):
        return target.with_suffix(
            target.suffix + ".bak"
        )

    # ---------------------------------------------------------
    # Repair
    # ---------------------------------------------------------

    def repair_file(
        self,
        relative_path: str,
        failure_context: str,
        diagnosis: str,
    ):
        """
        Ask AI to repair one controlled generated source file.
        """

        target = self._resolve_safe_file(
            relative_path
        )

        original_code = target.read_text(
            encoding="utf-8"
        )

        prompt = f"""
You are repairing an automatically generated
Python FastAPI backend.

Return ONLY the complete corrected Python file.

Rules:
- Do not use Markdown.
- Do not use triple backticks.
- Do not explain the solution.
- Do not modify unrelated behaviour.
- Preserve the existing architecture.
- Preserve existing imports whenever possible.
- Do not create new files.
- Do not rename modules.
- Fix only the failure described below.

File:
{relative_path}

Failure:
{failure_context}

Diagnosis:
{diagnosis}

Current file:

{original_code}
"""

        repaired_code = self.ai.generate(
            prompt
        )

        repaired_code = (
            self._clean_ai_response(
                repaired_code
            )
        )

        if not repaired_code.strip():

            raise RuntimeError(
                "AI returned empty repaired code."
            )

        if repaired_code.strip() == original_code.strip():

            raise RuntimeError(
                "AI repair did not change the file."
            )

        # -----------------------------------------------------
        # Backup original
        # -----------------------------------------------------

        backup = self._backup_path(
            target
        )

        shutil.copy2(
            target,
            backup,
        )

        # -----------------------------------------------------
        # Write candidate repair
        # -----------------------------------------------------

        target.write_text(
            repaired_code,
            encoding="utf-8",
        )

        # -----------------------------------------------------
        # Compile candidate
        # -----------------------------------------------------

        try:

            py_compile.compile(
                str(target),
                doraise=True,
            )

        except py_compile.PyCompileError as exc:

            shutil.copy2(
                backup,
                target,
            )

            backup.unlink(
                missing_ok=True
            )

            raise RuntimeError(
                "AI repair produced invalid "
                f"Python syntax: {exc}"
            ) from exc

        print(
            f"✅ Candidate repair compiled: "
            f"{relative_path}"
        )

        return {
            "success": True,
            "file": relative_path,
            "backup": str(backup),
        }

    # ---------------------------------------------------------
    # Commit
    # ---------------------------------------------------------

    def commit(
        self,
        relative_path: str,
    ):
        """
        Accept a validated repair and remove its backup.
        """

        target = self._resolve_safe_file(
            relative_path
        )

        backup = self._backup_path(
            target
        )

        if backup.exists():
            backup.unlink()

        print(
            f"✅ Repair committed: {relative_path}"
        )

        return True

    # ---------------------------------------------------------
    # Rollback
    # ---------------------------------------------------------

    def rollback(
        self,
        relative_path: str,
    ):
        """
        Restore original source from backup.
        """

        target = self._resolve_safe_file(
            relative_path
        )

        backup = self._backup_path(
            target
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

        backup.unlink(
            missing_ok=True
        )

        print(
            f"↩️ Repair rolled back: "
            f"{relative_path}"
        )

        return True

    # ---------------------------------------------------------
    # AI Response Cleanup
    # ---------------------------------------------------------

    @staticmethod
    def _clean_ai_response(
        response: str,
    ):
        """
        Remove accidental Markdown fences.
        """

        code = response.strip()

        if code.startswith(
            "```python"
        ):

            code = code[
                len("```python"):
            ]

        elif code.startswith(
            "```"
        ):

            code = code[3:]

        if code.endswith(
            "```"
        ):

            code = code[:-3]

        return code.strip()