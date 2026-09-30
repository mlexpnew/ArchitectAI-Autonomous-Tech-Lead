"""
Tests for Autonomous Self-Healing Loop, ErrorAnalyzer, and HealingEngine.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from self_healing.error_analyzer import ErrorAnalyzer
from self_healing.healing_engine import HealingEngine
from self_healing.retry_manager import SelfHealingLoop


def test_error_analyzer_traceback_parsing():
    analyzer = ErrorAnalyzer()

    # Traceback sample from pytest failure
    pytest_traceback = """
Traceback (most recent call last):
  File "/workspace/tests/test_items.py", line 12, in test_create_item
    response = client.post("/items", json={"name": "Book"})
  File "/workspace/app/api/item.py", line 45, in create_item
    raise ValueError("Missing field")
ValueError: Missing field
"""
    parsed_file = analyzer.parse_traceback_file(pytest_traceback)
    assert parsed_file == "app/api/item.py"

    # PyCompile syntax error sample
    compile_err = 'File "/workspace/app/models/account.py", line 14: SyntaxError: invalid syntax'
    parsed_compile = analyzer.parse_traceback_file(compile_err)
    assert parsed_compile == "app/models/account.py"

    # Fallback / explicit FILE:
    explicit_err = "Failure occurred. FILE: app/services/billing.py\nDetails: Null pointer"
    assert analyzer.parse_traceback_file(explicit_err) == "app/services/billing.py"


def test_error_analyzer_structured_diagnosis():
    analyzer = ErrorAnalyzer()
    failure = "SyntaxError: unexpected EOF while parsing in app/api/user.py"

    diagnosis = analyzer.analyze(failure)
    assert "root_cause" in diagnosis
    assert "target_file" in diagnosis
    assert "error_type" in diagnosis
    assert "fix_suggestion" in diagnosis
    assert diagnosis["target_file"] == "app/api/user.py"


def test_healing_engine_backup_and_rollback():
    with tempfile.TemporaryDirectory() as tmpdir:
        backend_dir = Path(tmpdir)
        app_dir = backend_dir / "app" / "api"
        app_dir.mkdir(parents=True)

        target = app_dir / "items.py"
        original_code = "def get_items():\n    return []\n"
        target.write_text(original_code, encoding="utf-8")

        healer = HealingEngine(backend_dir=str(backend_dir))

        # Manually create backup and test rollback
        backup_path = target.with_suffix(target.suffix + ".bak")
        backup_path.write_text(original_code, encoding="utf-8")
        target.write_text("broken code", encoding="utf-8")

        assert target.read_text() == "broken code"
        rolled_back = healer.rollback("app/api/items.py")
        assert rolled_back is True
        assert target.read_text() == original_code


def test_self_healing_loop_clean_run():
    with tempfile.TemporaryDirectory() as tmpdir:
        backend_dir = Path(tmpdir)
        # Create minimal required structure for ProjectValidator
        (backend_dir / "app").mkdir()
        (backend_dir / "app" / "models").mkdir()
        (backend_dir / "app" / "schemas").mkdir()
        (backend_dir / "app" / "repositories").mkdir()
        (backend_dir / "app" / "services").mkdir()
        (backend_dir / "app" / "api").mkdir()
        (backend_dir / "tests").mkdir()

        (backend_dir / "app" / "__init__.py").touch()
        (backend_dir / "app" / "main.py").write_text("# main\n", encoding="utf-8")
        (backend_dir / "app" / "database.py").write_text("# db\n", encoding="utf-8")
        (backend_dir / "app" / "models" / "__init__.py").touch()
        (backend_dir / "requirements.txt").write_text("fastapi\n", encoding="utf-8")
        (backend_dir / "tests" / "test_dummy.py").write_text("def test_ok(): pass\n", encoding="utf-8")

        with patch("orchestration.project_validator.ProjectValidator.run_tests") as mock_run_tests:
            mock_run_tests.return_value = {"passed": True, "returncode": 0, "stdout": "1 passed", "stderr": ""}

            loop = SelfHealingLoop(backend_dir=str(backend_dir), max_attempts=2)
            result = loop.run()

            assert result["healed"] is True
            assert result["clean_run"] is True
            assert result["attempts"] == 0


def test_self_healing_loop_successful_repair():
    with tempfile.TemporaryDirectory() as tmpdir:
        backend_dir = Path(tmpdir)
        (backend_dir / "app").mkdir()
        (backend_dir / "app" / "models").mkdir()
        (backend_dir / "app" / "schemas").mkdir()
        (backend_dir / "app" / "repositories").mkdir()
        (backend_dir / "app" / "services").mkdir()
        (backend_dir / "app" / "api").mkdir()
        (backend_dir / "tests").mkdir()

        (backend_dir / "app" / "__init__.py").touch()
        (backend_dir / "app" / "main.py").write_text("# main\n", encoding="utf-8")
        (backend_dir / "app" / "database.py").write_text("# db\n", encoding="utf-8")
        (backend_dir / "app" / "models" / "__init__.py").touch()
        (backend_dir / "requirements.txt").write_text("fastapi\n", encoding="utf-8")
        (backend_dir / "tests" / "test_dummy.py").write_text("def test_ok(): pass\n", encoding="utf-8")

        broken_file = backend_dir / "app" / "api" / "users.py"
        broken_file.write_text("def broken_func(\n", encoding="utf-8")  # syntax error

        loop = SelfHealingLoop(backend_dir=str(backend_dir), max_attempts=2)

        # Mock analyzer and healer to simulate a successful AI repair cycle
        with patch.object(loop.analyzer, "analyze") as mock_analyze, \
             patch.object(loop.healer, "heal_file") as mock_heal, \
             patch("orchestration.project_validator.ProjectValidator.run_tests") as mock_run_tests:

            mock_analyze.return_value = {
                "target_file": "app/api/users.py",
                "root_cause": "Unexpected EOF in function definition",
                "error_type": "SyntaxError",
                "fix_suggestion": "Close parentheses and add pass statement",
                "raw_diagnosis": "Fix syntax in app/api/users.py",
            }

            def simulate_heal(relative_path, failure_context, diagnosis):
                broken_file.write_text("def broken_func():\n    pass\n", encoding="utf-8")
                return {"success": True, "file": relative_path}

            mock_heal.side_effect = simulate_heal
            mock_run_tests.return_value = {"passed": True, "returncode": 0, "stdout": "1 passed", "stderr": ""}

            result = loop.run()

            assert result["healed"] is True
            assert result["clean_run"] is False
            assert result["attempts"] == 1
            assert result["healed_file"] == "app/api/users.py"
            assert "broken_func():" in broken_file.read_text()
