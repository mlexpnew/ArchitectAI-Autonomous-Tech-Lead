"""
Unit & Integration Tests for User Authentication and Multi-Tenant Workspaces
"""

import tempfile
import time
from pathlib import Path
import pytest

from auth.auth_manager import AuthManager
from auth.workspace_manager import WorkspaceManager
from auth.models import User, Workspace
from security_guardrails.rbac import Role


@pytest.fixture
def temp_auth_env():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        users_file = tmp_path / "users.json"
        workspaces_file = tmp_path / "workspaces.json"
        base_dir = tmp_path / "outputs" / "workspaces"

        wm = WorkspaceManager(workspaces_file=workspaces_file, base_dir=base_dir)
        am = AuthManager(users_file=users_file, workspace_manager=wm)

        yield am, wm, tmp_path


def test_password_hashing_and_verification(temp_auth_env):
    am, _, _ = temp_auth_env
    hashed = am.hash_password("SuperSecretPass123")
    assert "$" in hashed
    assert am.verify_password("SuperSecretPass123", hashed) is True
    assert am.verify_password("WrongPassword", hashed) is False


def test_default_seeded_personas(temp_auth_env):
    am, _, _ = temp_auth_env
    alex = am.authenticate_user("alex@architect.ai", "architect123")
    assert alex is not None
    assert alex.name == "Alex Chen"
    assert alex.role == Role.LEAD_ARCHITECT.value

    sarah = am.authenticate_user("sarah@auditor.corp", "audit123")
    assert sarah is not None
    assert sarah.role == Role.AUDITOR.value

    invalid = am.authenticate_user("alex@architect.ai", "wrongpass")
    assert invalid is None


def test_user_registration(temp_auth_env):
    am, wm, _ = temp_auth_env
    user = am.register_user(
        email="founder@acme.ai",
        password="founderpassword",
        name="Elena Rostova",
        role=Role.ADMIN.value,
        default_workspace_name="Acme AI Stealth",
    )
    assert user.email == "founder@acme.ai"
    assert user.name == "Elena Rostova"
    assert len(user.workspaces) == 1

    ws = wm.get_workspace(user.default_workspace_id)
    assert ws is not None
    assert ws.name == "Acme AI Stealth"
    assert ws.owner_id == user.user_id


def test_session_token_validation(temp_auth_env):
    am, _, _ = temp_auth_env
    user = am.get_user_by_email("alex@architect.ai")
    token = am.create_session_token(user, expires_in_hours=1)

    verified = am.verify_session_token(token)
    assert verified is not None
    assert verified.email == "alex@architect.ai"

    tampered_token = token[:-5] + "12345"
    assert am.verify_session_token(tampered_token) is None


def test_oauth_authentication(temp_auth_env):
    am, wm, _ = temp_auth_env
    user = am.oauth_authenticate(
        provider="google",
        email="google_user@gmail.com",
        name="Google Developer",
        avatar="🌐",
    )
    assert user.provider == "google"
    assert user.email == "google_user@gmail.com"

    # Subsequent login returns the existing account
    user2 = am.oauth_authenticate(
        provider="google",
        email="google_user@gmail.com",
        name="Google Developer",
    )
    assert user2.user_id == user.user_id


def test_workspace_project_isolation(temp_auth_env):
    _, wm, tmp_path = temp_auth_env
    ws1 = "ws_user_a"
    ws2 = "ws_user_b"

    wm.create_workspace(ws1, "User A Workspace", "usr_a")
    wm.create_workspace(ws2, "User B Workspace", "usr_b")

    dir_a = wm.get_project_dir(ws1, "FinTech_Service")
    dir_b = wm.get_project_dir(ws2, "FinTech_Service")

    # The directory paths must be strictly distinct and isolated
    assert dir_a != dir_b
    assert ws1 in str(dir_a)
    assert ws2 in str(dir_b)

    # Creating files in User A's workspace
    dir_a.mkdir(parents=True, exist_ok=True)
    (dir_a / "backend").mkdir(parents=True, exist_ok=True)
    (dir_a / "backend" / "user_a_only.py").write_text("print('user a')")

    # User B's workspace listing should NOT contain User A's files
    projects_b = wm.list_workspace_projects(ws2)
    assert len(projects_b) == 0

    projects_a = wm.list_workspace_projects(ws1)
    assert len(projects_a) == 1
    assert projects_a[0]["project_name"] == "FinTech_Service"


def test_workspace_team_membership_and_permissions(temp_auth_env):
    am, wm, _ = temp_auth_env
    alex = am.get_user_by_email("alex@architect.ai")
    dev = am.get_user_by_email("dev@startup.io")

    # Dev cannot access Alex's enterprise workspace initially
    assert wm.user_can_access_project(dev.user_id, "ws_enterprise_core", "FinTech_Banking_Ledger") is False

    # Add Dev as member
    assert wm.add_member("ws_enterprise_core", dev.user_id, "MEMBER") is True
    am.add_workspace_to_user(dev.user_id, "ws_enterprise_core")

    # Now Dev can access the workspace
    assert wm.user_can_access_project(dev.user_id, "ws_enterprise_core", "FinTech_Banking_Ledger") is True
    dev_workspaces = [w.workspace_id for w in wm.list_user_workspaces(dev.user_id)]
    assert "ws_enterprise_core" in dev_workspaces


def test_project_registration_in_workspace(temp_auth_env):
    _, wm, _ = temp_auth_env
    ws = wm.get_workspace("ws_enterprise_core")
    initial_count = len(ws.projects)

    wm.register_project_built("ws_enterprise_core", "Brand_New_Service")
    ws_updated = wm.get_workspace("ws_enterprise_core")
    assert "Brand_New_Service" in ws_updated.projects
    assert len(ws_updated.projects) == initial_count + 1
