"""
Generated Project Validator

Validates the structure, Python syntax,
required files, and generated pytest suite
of an ArchitectAI-generated backend.
"""

import os
from pathlib import Path
import py_compile
import subprocess
import sys


class ProjectValidator:

    REQUIRED_FILES = [
        "app/main.py",
        "app/database.py",
        "app/models/__init__.py",
        "requirements.txt",
    ]

    REQUIRED_DIRECTORIES = [
        "app/models",
        "app/schemas",
        "app/repositories",
        "app/services",
        "app/api",
        "tests",
    ]

    def __init__(
        self,
        backend_dir: str,
    ):
        self.backend_dir = Path(backend_dir)

    # ---------------------------------------------------------
    # Structure Validation
    # ---------------------------------------------------------

    def validate_structure(self):
        """
        Validate required files and directories.
        """

        errors = []

        if not self.backend_dir.exists():
            return [
                f"Backend directory does not exist: "
                f"{self.backend_dir}"
            ]

        for relative_path in self.REQUIRED_FILES:

            path = (
                self.backend_dir
                / relative_path
            )

            if not path.exists():
                errors.append(
                    f"Missing required file: "
                    f"{relative_path}"
                )

        for relative_path in self.REQUIRED_DIRECTORIES:

            path = (
                self.backend_dir
                / relative_path
            )

            if not path.is_dir():
                errors.append(
                    f"Missing required directory: "
                    f"{relative_path}"
                )

        return errors

    # ---------------------------------------------------------
    # Python Syntax Validation
    # ---------------------------------------------------------

    def validate_python_syntax(self):
        """
        Compile every generated Python file.
        """

        errors = []

        if not self.backend_dir.exists():
            return [
                "Cannot validate Python syntax because "
                "backend directory does not exist."
            ]

        for python_file in self.backend_dir.rglob(
            "*.py"
        ):

            try:

                py_compile.compile(
                    str(python_file),
                    doraise=True,
                )

            except py_compile.PyCompileError as exc:

                errors.append(
                    f"{python_file}: {exc}"
                )

        return errors

    # ---------------------------------------------------------
    # Test Existence Validation
    # ---------------------------------------------------------

    def validate_tests_exist(self):
        """
        Ensure generated tests exist.
        """

        tests_dir = (
            self.backend_dir
            / "tests"
        )

        if not tests_dir.exists():
            return [
                "Generated tests directory is missing."
            ]

        tests = list(
            tests_dir.glob(
                "test_*.py"
            )
        )

        if not tests:
            return [
                "No generated pytest tests found."
            ]

        return []

    # ---------------------------------------------------------
    # Runtime Test Execution
    # ---------------------------------------------------------

    def run_tests(self):
        """
        Run the generated backend pytest suite.
        """

        tests_dir = (
            self.backend_dir
            / "tests"
        )

        if not tests_dir.exists():

            return {
                "passed": False,
                "returncode": 1,
                "stdout": "",
                "stderr": (
                    "Tests directory does not exist."
                ),
            }

        print(
            "\n🧪 Running Generated Tests..."
        )

        env = os.environ.copy()
        backend_path = str(self.backend_dir.resolve())
        env["PYTHONPATH"] = (
            f"{backend_path}{os.pathsep}{env.get('PYTHONPATH', '')}"
            if env.get("PYTHONPATH")
            else backend_path
        )

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "tests",
                    "-q",
                    "-o",
                    f"rootdir={backend_path}",
                ],
                cwd=self.backend_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
            )

        except subprocess.TimeoutExpired:

            return {
                "passed": False,
                "returncode": -1,
                "stdout": "",
                "stderr": (
                    "Generated tests timed out."
                ),
            }

        except Exception as exc:

            return {
                "passed": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(exc),
            }

        passed = (
            result.returncode == 0
        )

        if passed:
            print(
                "✅ Generated tests passed"
            )

        else:
            print(
                "❌ Generated tests failed"
            )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return {
            "passed": passed,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    # ---------------------------------------------------------
    # Complete Validation Pipeline
    # ---------------------------------------------------------

    def validate(self):
        """
        Execute complete project validation.
        """

        print(
            "\n" + "=" * 60
        )

        print(
            "🔍 Validating Generated Project"
        )

        print(
            "=" * 60
        )

        errors = []

        # ---------------------------------------------
        # Static validation
        # ---------------------------------------------

        errors.extend(
            self.validate_structure()
        )

        errors.extend(
            self.validate_python_syntax()
        )

        errors.extend(
            self.validate_tests_exist()
        )

        # ---------------------------------------------
        # Runtime validation
        # ---------------------------------------------

        test_result = None

        if not errors:

            test_result = (
                self.run_tests()
            )

            if not test_result["passed"]:

                errors.append(
                    "Generated pytest suite failed."
                )

        # ---------------------------------------------
        # Validation failed
        # ---------------------------------------------

        if errors:

            print(
                "\n❌ Project validation failed"
            )

            for error in errors:

                print(
                    f" • {error}"
                )

            return {
                "valid": False,
                "errors": errors,
                "tests": test_result,
            }

        # ---------------------------------------------
        # Validation successful
        # ---------------------------------------------

        print(
            "\n✅ Generated project validation passed"
        )

        return {
            "valid": True,
            "errors": [],
            "tests": test_result,
        }