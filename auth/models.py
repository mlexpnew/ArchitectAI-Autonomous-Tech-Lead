"""
Authentication & Multi-Tenant Workspace Models

Defines data structures for Users, Workspaces, and Session tokens.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

from security_guardrails.rbac import Role


@dataclass
class User:
    """Authenticated user entity."""
    user_id: str
    email: str
    name: str
    hashed_password: str
    role: str = Role.LEAD_ARCHITECT.value
    avatar: str = "👨‍💻"
    workspaces: List[str] = field(default_factory=list)
    default_workspace_id: str = ""
    provider: str = "local"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "User":
        return cls(
            user_id=data["user_id"],
            email=data["email"],
            name=data["name"],
            hashed_password=data["hashed_password"],
            role=data.get("role", Role.LEAD_ARCHITECT.value),
            avatar=data.get("avatar", "👨‍💻"),
            workspaces=data.get("workspaces", []),
            default_workspace_id=data.get("default_workspace_id", ""),
            provider=data.get("provider", "local"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
        )


@dataclass
class Workspace:
    """Multi-tenant isolated workspace."""
    workspace_id: str
    name: str
    slug: str
    owner_id: str
    tier: str = "Pro"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    members: Dict[str, str] = field(default_factory=dict)  # user_id -> role
    projects: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Workspace":
        return cls(
            workspace_id=data["workspace_id"],
            name=data["name"],
            slug=data["slug"],
            owner_id=data["owner_id"],
            tier=data.get("tier", "Pro"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            members=data.get("members", {}),
            projects=data.get("projects", []),
        )
