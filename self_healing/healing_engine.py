"""
Healing Engine

Applies atomic, safe code repairs to generated source files,
verifies Python compilation, and manages backups and rollbacks.
"""

from pathlib import Path
import py_compile
import shutil
from typing import Any, Dict, Optional

from validation.python_validator import PythonValidator


class HealingEngine:
    """Safely repairs broken source files within a generated backend."""

    def __init__(self, backend_dir: str):
        self.backend_dir = Path(backend_dir).resolve()
        self._repair_engine = None

    @property
    def repair_engine(self):
        if self._repair_engine is None:
            from orchestration.code_repair_engine import CodeRepairEngine
            self._repair_engine = CodeRepairEngine(backend_dir=str(self.backend_dir))
        return self._repair_engine

    def heal_file(
        self,
        relative_path: str,
        failure_context: str,
        diagnosis: str,
    ) -> Dict[str, Any]:
        """
        Attempts to repair a specific relative file path using AI reflection.
        Creates a backup before modification and compiles the result.
        """
        target_path = self.backend_dir / relative_path
        if not target_path.exists():
            return {
                "success": False,
                "error": f"File does not exist: {relative_path}",
                "file": relative_path,
            }

        original_code = target_path.read_text(encoding="utf-8")

        try:
            # CodeRepairEngine safely handles .bak creation, resolution & compilation
            repair_result = self.repair_engine.repair_file(
                relative_path=relative_path,
                failure_context=failure_context,
                diagnosis=diagnosis,
            )

            repaired_code = target_path.read_text(encoding="utf-8")
            valid, msg = PythonValidator.validate(repaired_code)

            if not valid:
                self.rollback(relative_path)
                return {
                    "success": False,
                    "error": f"Repaired code failed syntax validation: {msg}",
                    "file": relative_path,
                }

            return {
                "success": True,
                "file": relative_path,
                "original_lines": len(original_code.splitlines()),
                "repaired_lines": len(repaired_code.splitlines()),
                "repair_result": repair_result,
            }

        except Exception as exc:
            self.rollback(relative_path)
            return {
                "success": False,
                "error": str(exc),
                "file": relative_path,
            }

    def commit(self, relative_path: str) -> bool:
        """Commits the repair by removing the .bak file."""
        return self.repair_engine.commit(relative_path)

    def rollback(self, relative_path: str) -> bool:
        """Restores the original file from the backup."""
        return self.repair_engine.rollback(relative_path)