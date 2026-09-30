"""
Enterprise Security Guardrails: Unified Manager & Compliance Facade

Orchestrates prompt injection defense, secret redaction, cryptographic audit logging,
and RBAC enforcement across the entire ArchitectAI execution lifecycle.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from security_guardrails.injection_shield import PromptInjectionShield, PromptInjectionBlockedException
from security_guardrails.secret_masker import SecretMasker
from security_guardrails.audit_logger import AuditLogger
from security_guardrails.rbac import Role, Permission, enforce_permission, has_permission


class GuardrailManager:
    """
    Central enterprise security manager enforcing zero-leakage, adversarial defense,
    and SOC2 audit traceability across all platform workflows.
    """

    def __init__(
        self,
        strict_injections: bool = True,
        mask_pii: bool = True,
        audit_log_path: Optional[Path | str] = None,
    ):
        self.injection_shield = PromptInjectionShield(strict_mode=strict_injections)
        self.secret_masker = SecretMasker(mask_pii=mask_pii)
        self.audit_logger = AuditLogger(log_file=audit_log_path)

    def validate_input(
        self,
        text: str,
        actor_role: str = "LEAD_ARCHITECT",
        actor_name: str = "User",
        resource: str = "ArchitectPipeline",
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Validates input text through the security defense pipeline:
        1. RBAC authorization verification
        2. Prompt injection threat scan
        3. Secret & PII detection and redaction
        4. Cryptographic audit trail recording

        Returns:
            Tuple of (sanitized_text, security_metadata)
        """
        # 1. RBAC check
        enforce_permission(actor_role, Permission.PIPELINE_GENERATE)

        # 2. Injection scan
        scan = self.injection_shield.scan(text)
        if not scan["is_safe"]:
            self.audit_logger.record_event(
                event_type="PROMPT_INJECTION_BLOCKED",
                action="Blocked adversarial prompt injection attempt",
                actor_role=actor_role,
                resource=resource,
                status="BLOCKED",
                details={
                    "threat_type": scan["threat_type"],
                    "threat_score": scan["threat_score"],
                    "matched_patterns": scan["matched_patterns"],
                    "actor_name": actor_name,
                },
            )
            raise PromptInjectionBlockedException(
                f"Adversarial prompt injection attempt blocked: {scan['threat_type']}",
                threat_type=scan["threat_type"],
                score=scan["threat_score"],
            )

        # 3. Secret & PII Redaction
        sanitized_text, redaction_count, detected_types = self.secret_masker.mask(text)
        if redaction_count > 0:
            self.audit_logger.record_event(
                event_type="SECRET_REDACTED",
                action="Redacted sensitive credentials or PII from prompt",
                actor_role=actor_role,
                resource=resource,
                status="FLAGGED",
                details={
                    "redaction_count": redaction_count,
                    "credential_types": detected_types,
                    "actor_name": actor_name,
                },
            )

        # 4. Record successful input acceptance
        self.audit_logger.record_event(
            event_type="INPUT_VALIDATION_PASSED",
            action="Input validated and cleared by security guardrails",
            actor_role=actor_role,
            resource=resource,
            status="SUCCESS",
            details={
                "actor_name": actor_name,
                "input_length": len(text),
                "redactions_applied": redaction_count,
            },
        )

        metadata = {
            "is_safe": True,
            "threat_score": scan["threat_score"],
            "redactions_count": redaction_count,
            "detected_secret_types": detected_types,
        }
        return sanitized_text, metadata

    def sanitize_output(
        self,
        output_text: str,
        actor_role: str = "LEAD_ARCHITECT",
        resource: str = "AICodeGenerator",
    ) -> Tuple[str, int]:
        """
        Sanitizes outgoing LLM responses and generated code to ensure
        no secrets or keys leak into logs or repositories.
        """
        sanitized_text, count, types = self.secret_masker.mask(output_text)
        if count > 0:
            self.audit_logger.record_event(
                event_type="OUTPUT_LEAKAGE_PREVENTED",
                action="Redacted credentials from LLM output stream",
                actor_role=actor_role,
                resource=resource,
                status="FLAGGED",
                details={"redactions": count, "types": types},
            )
        return sanitized_text, count

    def record_pipeline_lifecycle(
        self,
        action: str,
        project_name: str,
        actor_role: str = "LEAD_ARCHITECT",
        status: str = "SUCCESS",
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Convenience method to record pipeline execution milestones."""
        return self.audit_logger.record_event(
            event_type="PIPELINE_LIFECYCLE",
            action=action,
            actor_role=actor_role,
            resource=project_name,
            status=status,
            details=details or {},
        )

    def verify_ledger(self) -> Dict[str, Any]:
        """Audits the cryptographic SHA-256 hash chain."""
        return self.audit_logger.verify_integrity()

    def generate_soc2_report(self, target_path: Optional[Path | str] = None) -> str:
        """Generates and optionally persists a SOC2 Type II compliance report."""
        report = self.audit_logger.generate_soc2_compliance_report()
        if target_path:
            p = Path(target_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(report, encoding="utf-8")
        return report


_global_guardrails: Optional[GuardrailManager] = None


def get_guardrails() -> GuardrailManager:
    """Returns singleton instance of GuardrailManager."""
    global _global_guardrails
    if _global_guardrails is None:
        _global_guardrails = GuardrailManager()
    return _global_guardrails
