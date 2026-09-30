"""
Tests for Playwright & Cypress E2E Testing Suite Generator and Runner.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from generators.e2e_testing_generator import E2ETestingGenerator
from generators.project_packaging_generator import ProjectPackagingGenerator
from utils.e2e_manager import list_e2e_specs, run_cypress_e2e, run_playwright_e2e


def test_generate_playwright_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = E2ETestingGenerator(output_dir=tmpdir)
        gen.generate_playwright_config(project_name="FinTech Ledger")

        cfg_path = Path(tmpdir) / "frontend" / "playwright.config.ts"
        assert cfg_path.exists()
        content = cfg_path.read_text(encoding="utf-8")
        assert "defineConfig" in content
        assert "testDir: './e2e'" in content
        assert "'chromium'" in content
        assert "'firefox'" in content
        assert "'webkit'" in content
        assert "'Mobile Chrome'" in content
        assert "webServer:" in content


def test_generate_cypress_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = E2ETestingGenerator(output_dir=tmpdir)
        gen.generate_cypress_config(project_name="E-Commerce")

        f_dir = Path(tmpdir) / "frontend"
        assert (f_dir / "cypress.config.js").exists()
        assert (f_dir / "cypress" / "support" / "e2e.js").exists()
        assert (f_dir / "cypress" / "support" / "commands.js").exists()

        commands_content = (f_dir / "cypress" / "support" / "commands.js").read_text(encoding="utf-8")
        assert "Cypress.Commands.add('getByTestId'" in commands_content
        assert "Cypress.Commands.add('login'" in commands_content


def test_generate_playwright_and_cypress_specs():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = E2ETestingGenerator(output_dir=tmpdir)

        # Mock blueprint
        f1 = MagicMock()
        f1.name = "patient_name"
        f1.type = "string"

        f2 = MagicMock()
        f2.name = "age"
        f2.type = "integer"

        f3 = MagicMock()
        f3.name = "billing_amount"
        f3.type = "decimal"

        e1 = MagicMock()
        e1.name = "Patient"
        e1.fields = [f1, f2, f3]

        bp = MagicMock()
        bp.entities = [e1]

        gen.generate_playwright_specs(project_name="Hospital Platform", blueprint=bp)
        gen.generate_cypress_specs(project_name="Hospital Platform", blueprint=bp)

        f_dir = Path(tmpdir) / "frontend"
        # Playwright checks
        assert (f_dir / "e2e" / "smoke.spec.ts").exists()
        patient_pw = f_dir / "e2e" / "patient.spec.ts"
        assert patient_pw.exists()

        pw_content = patient_pw.read_text(encoding="utf-8")
        assert "test.describe('Patient Management E2E Workflows'" in pw_content
        assert "[@smoke]" in pw_content
        assert "[@crud]" in pw_content
        assert "[@validation]" in pw_content
        assert "[@mock]" in pw_content
        assert "patient_nameInput" in pw_content
        assert "billing_amountInput" in pw_content

        # Cypress checks
        assert (f_dir / "cypress" / "e2e" / "smoke.cy.js").exists()
        patient_cy = f_dir / "cypress" / "e2e" / "patient.cy.js"
        assert patient_cy.exists()

        cy_content = patient_cy.read_text(encoding="utf-8")
        assert "describe('Patient Management E2E (Cypress)'" in cy_content
        assert "cy.intercept('GET', '**/api/**/patients*'" in cy_content


def test_generate_package_json_and_ci_workflow():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = E2ETestingGenerator(output_dir=tmpdir)
        gen.generate_package_json(project_name="Library System")
        gen.generate_ci_workflow(project_name="Library System")
        gen.generate_readme(project_name="Library System")

        f_dir = Path(tmpdir) / "frontend"
        pkg_file = f_dir / "package.json"
        assert pkg_file.exists()
        pkg_content = pkg_file.read_text(encoding="utf-8")
        assert '"test:e2e": "playwright test"' in pkg_content
        assert '"cypress:run": "cypress run"' in pkg_content
        assert '"@playwright/test"' in pkg_content
        assert '"cypress"' in pkg_content

        ci_file = f_dir / ".github" / "workflows" / "e2e.yml"
        assert ci_file.exists()
        ci_content = ci_file.read_text(encoding="utf-8")
        assert "playwright-e2e" in ci_content
        assert "cypress-e2e" in ci_content

        readme_file = f_dir / "README.md"
        assert readme_file.exists()
        assert "Playwright" in readme_file.read_text(encoding="utf-8")


def test_e2e_manager_discovery_and_runner():
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = E2ETestingGenerator(output_dir=tmpdir)

        f1 = MagicMock()
        f1.name = "title"
        f1.type = "string"

        e1 = MagicMock()
        e1.name = "Article"
        e1.fields = [f1]

        bp = MagicMock()
        bp.entities = [e1]

        gen.generate(project_name="Blog API", blueprint=bp)

        f_dir = Path(tmpdir) / "frontend"
        specs = list_e2e_specs(f_dir)

        assert specs["exists"] is True
        assert specs["playwright"]["config"] == "playwright.config.ts"
        assert specs["cypress"]["config"] == "cypress.config.js"
        assert len(specs["playwright"]["specs"]) == 2  # smoke + article
        assert len(specs["cypress"]["specs"]) == 2

        # Run Playwright suite
        pw_result = run_playwright_e2e(f_dir)
        assert pw_result["success"] is True
        assert pw_result["passed"] > 0
        assert pw_result["failed"] == 0
        assert "chromium" in pw_result["stdout"]
        assert len(pw_result["executed_tests"]) > 0

        # Run Cypress suite
        cy_result = run_cypress_e2e(f_dir)
        assert cy_result["success"] is True
        assert cy_result["passed"] > 0
        assert cy_result["failed"] == 0
        assert "All specs passed" in cy_result["stdout"]

        # Run with nonexistent directory
        bad_dir = Path(tmpdir) / "does_not_exist"
        bad_res = run_playwright_e2e(bad_dir)
        assert bad_res["success"] is False
        assert "not found" in bad_res["stderr"]
