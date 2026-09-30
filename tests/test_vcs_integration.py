"""
Tests for Enterprise VCS Integration, Git Staging, and Pull Request Generator.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from utils.vcs_manager import PRTemplateBuilder, VCSManager


def test_pr_template_builder():
    with tempfile.TemporaryDirectory() as tmpdir:
        p_dir = Path(tmpdir)
        backend_dir = p_dir / "backend"
        backend_dir.mkdir()

        # Mock manifest
        manifest = {
            "entities": [
                {
                    "name": "Invoice",
                    "fields": [{"name": "id"}, {"name": "amount"}, {"name": "due_date"}],
                },
                {
                    "name": "Client",
                    "fields": [{"name": "id"}, {"name": "company_name"}],
                },
            ]
        }
        (backend_dir / "architectai_manifest.json").write_text(
            '{"entities": [{"name": "Invoice", "fields": [{"name": "amount"}]}]}',
            encoding="utf-8",
        )

        body = PRTemplateBuilder.build(
            project_name="Billing_Platform",
            project_dir=p_dir,
            branch_name="feat/billing-core",
        )

        assert "## 🚀 Overview & System Architecture" in body
        assert "Billing Platform" in body
        assert "Invoice" in body
        assert "SQLAlchemy 2.0" in body
        assert "FastAPI" in body
        assert "Playwright" in body
        assert "Cypress" in body
        assert "Security & Compliance Checklist" in body


def test_prepare_local_repository():
    with tempfile.TemporaryDirectory() as tmpdir:
        p_dir = Path(tmpdir)
        (p_dir / "README.md").write_text("# Demo Project\n", encoding="utf-8")
        (p_dir / "app.py").write_text("print('hello')\n", encoding="utf-8")

        vcs = VCSManager(project_dir=p_dir)
        res = vcs.prepare_local_repository(project_name="Demo Project", branch_name="feat/init")

        assert res["success"] is True
        assert res["branch"] == "feat/init"
        assert res["base_branch"] == "main"
        assert (p_dir / ".git").exists()
        assert len(res["commit_sha"]) >= 6


def test_github_pr_simulation_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        p_dir = Path(tmpdir)
        (p_dir / "README.md").write_text("# Test\n", encoding="utf-8")

        vcs = VCSManager(project_dir=p_dir)
        result = vcs.push_and_create_github_pr(
            token="",
            project_name="Hospital_Management_System",
            repo_name="hospital-management-system",
            simulation_mode=True,
        )

        assert result["success"] is True
        assert result["simulation"] is True
        assert result["provider"] == "GitHub"
        assert "hospital-management-system" in result["repo_url"]
        assert "/pull/1" in result["pr_url"]
        assert result["pr_number"] == 1
        assert "Overview & System Architecture" in result["pr_body"]


def test_github_pr_mock_api():
    with tempfile.TemporaryDirectory() as tmpdir:
        p_dir = Path(tmpdir)
        (p_dir / "README.md").write_text("# Test\n", encoding="utf-8")

        vcs = VCSManager(project_dir=p_dir)

        # Mock httpx responses for user, repo check (404), repo create (201), and PR create (201)
        mock_user = MagicMock(status_code=200, json=lambda: {"login": "octocat"})
        mock_repo_check = MagicMock(status_code=404)
        mock_repo_create = MagicMock(status_code=201, json=lambda: {"html_url": "https://github.com/octocat/test-api"})
        mock_pr_create = MagicMock(status_code=201, json=lambda: {"html_url": "https://github.com/octocat/test-api/pull/42", "number": 42})

        with patch("httpx.Client.get") as mock_get, \
             patch("httpx.Client.post") as mock_post, \
             patch.object(vcs, "_run_git") as mock_git:

            mock_git.return_value = MagicMock(returncode=0, stdout="abc1234\n", stderr="")
            mock_get.side_effect = [mock_user, mock_repo_check]
            mock_post.side_effect = [mock_repo_create, mock_pr_create]

            result = vcs.push_and_create_github_pr(
                token="ghp_fake_token_12345",
                project_name="Test API",
                repo_name="test-api",
                simulation_mode=False,
            )

            assert result["success"] is True
            assert result["simulation"] is False
            assert result["pr_number"] == 42
            assert result["pr_url"] == "https://github.com/octocat/test-api/pull/42"
            assert result["repo_full_name"] == "octocat/test-api"
