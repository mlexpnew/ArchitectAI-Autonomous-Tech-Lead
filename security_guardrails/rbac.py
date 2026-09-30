"""
Enterprise Security Guardrails: Role-Based Access Control (RBAC)

Defines system roles, granular permissions, and authorization enforcement
for Admin, Lead Architect, Developer, and Auditor actors.
"""

from enum import Enum
from typing import Dict, Set


class Role(str, Enum):
    ADMIN = "ADMIN"
    LEAD_ARCHITECT = "LEAD_ARCHITECT"
    DEVELOPER = "DEVELOPER"
    AUDITOR = "AUDITOR"


class Permission(str, Enum):
    PIPELINE_GENERATE = "PIPELINE_GENERATE"
    PUSH_VCS_PR = "PUSH_VCS_PR"
    CONFIGURE_SECRETS = "CONFIGURE_SECRETS"
    VIEW_AUDIT_LOGS = "VIEW_AUDIT_LOGS"
    VERIFY_AUDIT_CHAIN = "VERIFY_AUDIT_CHAIN"
    RUN_BENCHMARKS = "RUN_BENCHMARKS"
    VIEW_TELEMETRY = "VIEW_TELEMETRY"
    TRIGGER_SELF_HEALING = "TRIGGER_SELF_HEALING"
    EXPORT_DATA_ROOM = "EXPORT_DATA_ROOM"


ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.ADMIN: {
        Permission.PIPELINE_GENERATE,
        Permission.PUSH_VCS_PR,
        Permission.CONFIGURE_SECRETS,
        Permission.VIEW_AUDIT_LOGS,
        Permission.VERIFY_AUDIT_CHAIN,
        Permission.RUN_BENCHMARKS,
        Permission.VIEW_TELEMETRY,
        Permission.TRIGGER_SELF_HEALING,
        Permission.EXPORT_DATA_ROOM,
    },
    Role.LEAD_ARCHITECT: {
        Permission.PIPELINE_GENERATE,
        Permission.PUSH_VCS_PR,
        Permission.VIEW_AUDIT_LOGS,
        Permission.RUN_BENCHMARKS,
        Permission.VIEW_TELEMETRY,
        Permission.TRIGGER_SELF_HEALING,
        Permission.EXPORT_DATA_ROOM,
    },
    Role.DEVELOPER: {
        Permission.PIPELINE_GENERATE,
        Permission.VIEW_TELEMETRY,
        Permission.TRIGGER_SELF_HEALING,
    },
    Role.AUDITOR: {
        Permission.VIEW_AUDIT_LOGS,
        Permission.VERIFY_AUDIT_CHAIN,
        Permission.VIEW_TELEMETRY,
        Permission.EXPORT_DATA_ROOM,
    },
}


class AccessDeniedException(PermissionError):
    """Raised when an actor attempts an action unauthorized for their RBAC role."""
    def __init__(self, role: str, permission: str):
        super().__init__(f"Access denied: Role '{role}' lacks permission '{permission}'.")
        self.role = role
        self.permission = permission


def has_permission(role: str | Role, permission: str | Permission) -> bool:
    """Verifies whether a given role holds the specified permission."""
    try:
        r = Role(role.upper()) if isinstance(role, str) else role
        p = Permission(permission) if isinstance(permission, str) else permission
        return p in ROLE_PERMISSIONS.get(r, set())
    except Exception:
        return False


def enforce_permission(role: str | Role, permission: str | Permission) -> None:
    """Enforces authorization check, raising AccessDeniedException if not permitted."""
    if not has_permission(role, permission):
        r_str = role.value if isinstance(role, Role) else str(role)
        p_str = permission.value if isinstance(permission, Permission) else str(permission)
        raise AccessDeniedException(role=r_str, permission=p_str)
