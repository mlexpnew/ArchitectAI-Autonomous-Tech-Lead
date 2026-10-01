"""
Multi-Tenant Workspace & Project Isolation Manager

Ensures complete tenant separation: User A cannot view, modify, or overwrite
User B's generated code, telemetry, or cloud manifests.
"""

from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import re
import shutil
from typing import Dict, List, Optional

from auth.models import Workspace

logger = logging.getLogger(__name__)

DATA_DIR = Path("data")
WORKSPACES_FILE = DATA_DIR / "workspaces.json"
BASE_WORKSPACES_DIR = Path("outputs") / "workspaces"


class WorkspaceManager:
    """Manages multi-tenant workspaces and isolated filesystem project storage."""

    def __init__(
        self,
        workspaces_file: Optional[Path] = None,
        base_dir: Optional[Path] = None,
    ):
        self.workspaces_file = workspaces_file or WORKSPACES_FILE
        self.base_dir = base_dir or BASE_WORKSPACES_DIR
        self.workspaces_file.parent.mkdir(parents=True, exist_ok=True)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.workspaces: Dict[str, Workspace] = {}
        self._load_or_seed()

    # =========================================================================
    # Persistence & Seeding
    # =========================================================================

    def _load_or_seed(self):
        """Loads workspace records from JSON or seeds initial enterprise workspaces."""
        if self.workspaces_file.exists():
            try:
                data = json.loads(self.workspaces_file.read_text(encoding="utf-8"))
                for w_dict in data:
                    w = Workspace.from_dict(w_dict)
                    self.workspaces[w.workspace_id] = w
                if self.workspaces:
                    return
            except Exception as e:
                logger.warning(f"Failed to load workspaces: {e}. Reseeding defaults.")

        self._seed_default_workspaces()

    def _seed_default_workspaces(self):
        """Seeds default multi-tenant workspaces for instant enterprise evaluation."""
        defaults = [
            Workspace(
                workspace_id="ws_enterprise_core",
                name="🏢 Enterprise Core Platform",
                slug="enterprise-core",
                owner_id="usr_alex_chen",
                tier="Enterprise",
                members={"usr_alex_chen": "OWNER", "usr_admin_root": "ADMIN"},
                projects=["FinTech_Banking_Ledger", "Hospital_Management_System"],
            ),
            Workspace(
                workspace_id="ws_alex_personal",
                name="👤 Alex Chen (Personal)",
                slug="alex-personal",
                owner_id="usr_alex_chen",
                tier="Pro",
                members={"usr_alex_chen": "OWNER"},
                projects=[],
            ),
            Workspace(
                workspace_id="ws_compliance_lab",
                name="🛡️ SOC2 Compliance Lab",
                slug="compliance-lab",
                owner_id="usr_sarah_vance",
                tier="Enterprise",
                members={"usr_sarah_vance": "OWNER", "usr_admin_root": "ADMIN"},
                projects=["Security_Audit_Gateway"],
            ),
            Workspace(
                workspace_id="ws_dev_rapid",
                name="⚡ DevOps Rapid Prototyping",
                slug="dev-rapid",
                owner_id="usr_devin_miller",
                tier="Pro",
                members={"usr_devin_miller": "OWNER"},
                projects=["ECommerce_Platform", "Ride_Sharing_Telemetry"],
            ),
        ]

        self.workspaces = {w.workspace_id: w for w in defaults}
        self._save()

        # Seed initial directory structures and link standard projects if available
        for ws in defaults:
            ws_dir = self.get_workspace_dir(ws.workspace_id)
            ws_dir.mkdir(parents=True, exist_ok=True)
            self._link_initial_projects(ws)

    def _link_initial_projects(self, workspace: Workspace):
        """Ensures seeded workspaces have their sample projects linked."""
        ws_dir = self.get_workspace_dir(workspace.workspace_id)
        global_outputs = Path("outputs")

        for proj in workspace.projects:
            target_proj_dir = ws_dir / proj
            global_proj_dir = global_outputs / proj
            if not target_proj_dir.exists() and global_proj_dir.exists() and (global_proj_dir / "backend").exists():
                try:
                    shutil.copytree(global_proj_dir, target_proj_dir)
                except Exception as e:
                    logger.debug(f"Could not copy initial project {proj}: {e}")

    def _save(self):
        """Persists workspaces to disk."""
        data = [w.to_dict() for w in self.workspaces.values()]
        self.workspaces_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # =========================================================================
    # Workspace Operations
    # =========================================================================

    def create_workspace(
        self,
        workspace_id: str,
        name: str,
        owner_id: str,
        tier: str = "Pro",
    ) -> Workspace:
        """Creates a new isolated workspace."""
        slug = re.sub(r"[^a-zA-Z0-9_-]", "-", name.lower()).strip("-")
        ws = Workspace(
            workspace_id=workspace_id,
            name=name,
            slug=slug,
            owner_id=owner_id,
            tier=tier,
            members={owner_id: "OWNER"},
            projects=[],
        )
        self.workspaces[workspace_id] = ws
        self._save()

        ws_dir = self.get_workspace_dir(workspace_id)
        ws_dir.mkdir(parents=True, exist_ok=True)
        return ws

    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        return self.workspaces.get(workspace_id)

    def list_user_workspaces(self, user_id: str) -> List[Workspace]:
        """Returns all workspaces the user owns or is a member of."""
        matched = []
        for ws in self.workspaces.values():
            if ws.owner_id == user_id or user_id in ws.members:
                matched.append(ws)
        return matched

    def add_member(self, workspace_id: str, user_id: str, role: str = "MEMBER") -> bool:
        """Adds or updates a member in the workspace."""
        ws = self.get_workspace(workspace_id)
        if not ws:
            return False
        ws.members[user_id] = role
        self._save()
        return True

    # =========================================================================
    # Project Isolation & Directory Pathing
    # =========================================================================

    def get_workspace_dir(self, workspace_id: str) -> Path:
        """Returns the isolated root directory for a workspace."""
        path = self.base_dir / workspace_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_project_dir(self, workspace_id: str, project_name: str) -> Path:
        """Returns the isolated directory for a specific project within a workspace."""
        safe_name = project_name.replace(" ", "_")
        return self.get_workspace_dir(workspace_id) / safe_name

    def list_workspace_projects(self, workspace_id: str) -> List[Dict]:
        """
        Lists only projects contained inside this workspace.
        User A cannot see User B's projects.
        """
        ws_dir = self.get_workspace_dir(workspace_id)
        projects = []

        if not ws_dir.exists():
            return projects

        for p in ws_dir.iterdir():
            if p.is_dir() and not p.name.startswith("."):
                backend_dir = p / "backend"
                models_dir = backend_dir / "app" / "models"
                model_count = len(list(models_dir.glob("*.py"))) if models_dir.exists() else 0
                file_count = sum(1 for _ in p.rglob("*") if _.is_file())

                projects.append({
                    "project_name": p.name,
                    "workspace_id": workspace_id,
                    "path": str(p),
                    "file_count": file_count,
                    "model_count": max(0, model_count - 1),  # exclude __init__.py
                    "has_backend": backend_dir.exists(),
                    "archive_exists": (p / "exports" / f"{p.name.lower()}.zip").exists(),
                    "last_modified": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
                })

        return sorted(projects, key=lambda x: x["last_modified"], reverse=True)

    def register_project_built(self, workspace_id: str, project_name: str):
        """Records a new project build under the specified workspace."""
        ws = self.get_workspace(workspace_id)
        if ws and project_name not in ws.projects:
            ws.projects.append(project_name)
            self._save()

    def user_can_access_project(
        self,
        user_id: str,
        workspace_id: str,
        project_name: str,
    ) -> bool:
        """Validates that the user has authorization to access this workspace's project."""
        ws = self.get_workspace(workspace_id)
        if not ws:
            return False
        return ws.owner_id == user_id or user_id in ws.members


# Global Singleton
_workspace_manager: Optional[WorkspaceManager] = None


def get_workspace_manager() -> WorkspaceManager:
    global _workspace_manager
    if _workspace_manager is None:
        _workspace_manager = WorkspaceManager()
    return _workspace_manager
