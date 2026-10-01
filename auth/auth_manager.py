"""
Authentication Manager

Enterprise authentication provider supporting email/password, salted PBKDF2 hashing,
OAuth2 (Google, GitHub, Supabase), secure session tokens, and RBAC role mapping.
"""

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import logging
import os
from pathlib import Path
import secrets
import time
from typing import Any, Dict, List, Optional, Tuple

from auth.models import User
from config.settings import settings
from security_guardrails.rbac import Role

logger = logging.getLogger(__name__)

STORAGE_DIR = Path("data")
USERS_FILE = STORAGE_DIR / "users.json"
SESSION_SECRET = os.getenv("AUTH_SECRET", "architectai_sec_enterprise_auth_token_key_2026")


class AuthManager:
    """Manages user registration, authentication, OAuth, and sessions."""

    def __init__(
        self,
        users_file: Optional[Path] = None,
        workspace_manager: Optional[Any] = None,
    ):
        self.users_file = users_file or USERS_FILE
        self.workspace_manager = workspace_manager
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        self.users: Dict[str, User] = {}
        self._load_or_seed()

    # =========================================================================
    # Cryptographic Password Utilities
    # =========================================================================

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> str:
        """Hashes password using PBKDF2-HMAC-SHA256 with 100,000 rounds."""
        if not salt:
            salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations=100_000,
        ).hex()
        return f"{salt}${pwd_hash}"

    @classmethod
    def verify_password(cls, password: str, stored_hash: str) -> bool:
        """Verifies password against stored salt$hash string."""
        try:
            if "$" not in stored_hash:
                return False
            salt, _ = stored_hash.split("$", 1)
            expected = cls.hash_password(password, salt=salt)
            return hmac.compare_digest(expected, stored_hash)
        except Exception:
            return False

    # =========================================================================
    # Session Token Management
    # =========================================================================

    @staticmethod
    def create_session_token(user: User, expires_in_hours: int = 24) -> str:
        """Generates an HMAC-SHA256 signed session token containing user_id and expiry."""
        expires_at = int(time.time()) + (expires_in_hours * 3600)
        payload = f"{user.user_id}:{user.email}:{expires_at}"
        sig = hmac.new(
            SESSION_SECRET.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return f"{payload}:{sig}"

    def verify_session_token(self, token: str) -> Optional[User]:
        """Validates signature and expiry of session token; returns User if valid."""
        try:
            parts = token.split(":")
            if len(parts) != 4:
                return None
            user_id, email, expires_at_str, sig = parts
            if int(expires_at_str) < time.time():
                return None  # Expired

            payload = f"{user_id}:{email}:{expires_at_str}"
            expected_sig = hmac.new(
                SESSION_SECRET.encode("utf-8"),
                payload.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            if not hmac.compare_digest(sig, expected_sig):
                return None

            return self.get_user_by_id(user_id)
        except Exception:
            return None

    # =========================================================================
    # User Persistence & Seeding
    # =========================================================================

    def _load_or_seed(self):
        """Loads users from JSON storage or seeds initial enterprise persona accounts."""
        if self.users_file.exists():
            try:
                data = json.loads(self.users_file.read_text(encoding="utf-8"))
                for u_dict in data:
                    u = User.from_dict(u_dict)
                    self.users[u.email.lower()] = u
                if self.users:
                    return
            except Exception as e:
                logger.warning(f"Failed to read users file: {e}. Reseeding defaults.")

        # Seed Default Enterprise Personas
        self._seed_default_users()

    def _seed_default_users(self):
        """Seeds standard enterprise accounts for immediate 1-click evaluation."""
        defaults = [
            User(
                user_id="usr_alex_chen",
                email="alex@architect.ai",
                name="Alex Chen",
                hashed_password=self.hash_password("architect123"),
                role=Role.LEAD_ARCHITECT.value,
                avatar="👨‍💼",
                workspaces=["ws_enterprise_core", "ws_alex_personal"],
                default_workspace_id="ws_enterprise_core",
                provider="local",
            ),
            User(
                user_id="usr_sarah_vance",
                email="sarah@auditor.corp",
                name="Sarah Vance",
                hashed_password=self.hash_password("audit123"),
                role=Role.AUDITOR.value,
                avatar="👩‍⚖️",
                workspaces=["ws_compliance_lab"],
                default_workspace_id="ws_compliance_lab",
                provider="local",
            ),
            User(
                user_id="usr_devin_miller",
                email="dev@startup.io",
                name="Devin Miller",
                hashed_password=self.hash_password("dev123"),
                role=Role.DEVELOPER.value,
                avatar="👨‍💻",
                workspaces=["ws_dev_rapid"],
                default_workspace_id="ws_dev_rapid",
                provider="local",
            ),
            User(
                user_id="usr_admin_root",
                email="admin@architect.ai",
                name="Enterprise Admin",
                hashed_password=self.hash_password("admin123"),
                role=Role.ADMIN.value,
                avatar="🛡️",
                workspaces=["ws_enterprise_core", "ws_compliance_lab", "ws_dev_rapid"],
                default_workspace_id="ws_enterprise_core",
                provider="local",
            ),
        ]

        self.users = {u.email.lower(): u for u in defaults}
        self._save()

    def _save(self):
        """Persists current user dictionary to disk."""
        data = [u.to_dict() for u in self.users.values()]
        self.users_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def save_users(self):
        """Public alias to persist current user dictionary to disk."""
        self._save()

    def add_workspace_to_user(self, user_id: str, workspace_id: str):
        """Associates a workspace ID with a user."""
        u = self.get_user_by_id(user_id)
        if u and workspace_id not in u.workspaces:
            u.workspaces.append(workspace_id)
            self._save()

    # =========================================================================
    # Auth Workflows
    # =========================================================================

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticates user with email and password."""
        email_clean = email.strip().lower()
        user = self.users.get(email_clean)
        if not user:
            return None
        if self.verify_password(password, user.hashed_password):
            return user
        return None

    def register_user(
        self,
        email: str,
        password: str,
        name: str,
        role: str = Role.LEAD_ARCHITECT.value,
        default_workspace_name: Optional[str] = None,
    ) -> User:
        """Registers a new user and creates their personal isolated workspace."""
        email_clean = email.strip().lower()
        if email_clean in self.users:
            raise ValueError(f"User with email '{email}' already exists.")

        user_id = f"usr_{secrets.token_hex(6)}"
        ws_id = f"ws_{secrets.token_hex(6)}"

        user = User(
            user_id=user_id,
            email=email_clean,
            name=name.strip(),
            hashed_password=self.hash_password(password),
            role=role,
            avatar="🚀",
            workspaces=[ws_id],
            default_workspace_id=ws_id,
            provider="local",
        )

        self.users[email_clean] = user
        self._save()

        # Initialize personal workspace
        from auth.workspace_manager import get_workspace_manager
        ws_mgr = self.workspace_manager or get_workspace_manager()
        ws_name = default_workspace_name or f"{name.strip()}'s Workspace"
        ws_mgr.create_workspace(
            workspace_id=ws_id,
            name=ws_name,
            owner_id=user_id,
            tier="Pro",
        )

        return user

    def oauth_authenticate(
        self,
        provider: str,
        email: str,
        name: str,
        avatar: str = "🌐",
    ) -> User:
        """Authenticates or automatically onboards a user via OAuth (Google, GitHub, Clerk, Supabase)."""
        email_clean = email.strip().lower()
        user = self.users.get(email_clean)

        if user:
            return user

        # Auto-provision new OAuth user
        user_id = f"usr_{provider}_{secrets.token_hex(6)}"
        ws_id = f"ws_{secrets.token_hex(6)}"

        user = User(
            user_id=user_id,
            email=email_clean,
            name=name.strip(),
            hashed_password=self.hash_password(secrets.token_hex(32)),  # Random password
            role=Role.LEAD_ARCHITECT.value,
            avatar=avatar,
            workspaces=[ws_id],
            default_workspace_id=ws_id,
            provider=provider,
        )

        self.users[email_clean] = user
        self._save()

        from auth.workspace_manager import get_workspace_manager
        ws_mgr = self.workspace_manager or get_workspace_manager()
        ws_mgr.create_workspace(
            workspace_id=ws_id,
            name=f"{name.strip()}'s Workspace",
            owner_id=user_id,
            tier="Pro",
        )

        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        for u in self.users.values():
            if u.user_id == user_id:
                return u
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users.get(email.strip().lower())

    def list_users(self) -> List[User]:
        return list(self.users.values())


# Global Singleton
_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
