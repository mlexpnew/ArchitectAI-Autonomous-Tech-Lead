"""
Autonomous Security Agent

Executes automated Static Application Security Testing (SAST),
hardcoded secret scanning, and OWASP Top 10 vulnerability checks
on generated microservices.
"""

from pathlib import Path
import re
from typing import Any, Dict, List

from agents.base_agent import BaseAgent
from security_guardrails.secret_masker import SecretMasker
from security_guardrails.guardrail_manager import get_guardrails


class SecurityAgent(BaseAgent):
    """
    Autonomous SAST & Security Compliance Agent.
    Audits generated codebases for dangerous sinks, credential leaks, and insecure configs.
    """

    DANGEROUS_PATTERNS = [
        ("INSECURE_EVAL_EXEC", r"\b(eval|exec)\s*\(", "Use of dangerous dynamic execution sink"),
        ("COMMAND_INJECTION", r"subprocess\.(?:Popen|call|run)\([^)]*shell\s*=\s*True", "Shell command injection risk"),
        ("SYSTEM_COMMAND", r"os\.system\s*\(", "Insecure os.system invocation"),
        ("SQL_INJECTION_RISK", r"\.execute\(\s*f[\"'].*?\{.*?\}", "Possible SQL string interpolation instead of parameterized queries"),
        ("PERMISSIVE_CORS", r"allow_origins\s*=\s*\[\s*[\"']\*[\"']\s*\]", "Wildcard CORS origin detected"),
    ]

    def __init__(self, workspace, bus):
        super().__init__(workspace, bus)
        self.masker = SecretMasker()

    @property
    def name(self):
        return "security"

    def audit_directory(self, target_dir: Path | str) -> Dict[str, Any]:
        """Performs comprehensive SAST and secret scan across a project directory."""
        target = Path(target_dir)
        findings = []
        files_scanned = 0

        if not target.exists():
            return {
                "status": "SKIPPED",
                "reason": f"Directory not found: {target}",
                "findings": [],
                "files_scanned": 0,
            }

        for py_file in target.rglob("*.py"):
            files_scanned += 1
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            rel_path = str(py_file)
            try:
                rel_path = str(py_file.relative_to(target))
            except Exception:
                pass

            # 1. Hardcoded secret check
            _, count, types = self.masker.mask(content)
            if count > 0:
                findings.append({
                    "file": rel_path,
                    "severity": "CRITICAL",
                    "type": "HARDCODED_CREDENTIAL",
                    "description": f"Detected {count} sensitive credential pattern(s): {', '.join(types)}",
                })

            # 2. Dangerous function / sink checks
            for check_id, pattern, desc in self.DANGEROUS_PATTERNS:
                matches = re.finditer(pattern, content)
                for m in matches:
                    findings.append({
                        "file": rel_path,
                        "severity": "HIGH",
                        "type": check_id,
                        "description": desc,
                        "snippet": m.group(0)[:50],
                    })

        status = "PASSED" if not findings else "WARNINGS_FOUND"
        return {
            "status": status,
            "target_dir": str(target),
            "files_scanned": files_scanned,
            "total_findings": len(findings),
            "findings": findings,
        }

    def execute(self, project):
        print("🔒 Security Agent — Running Enterprise SAST & Compliance Audit...")

        # If project has output directory or workspace
        target_dir = Path(getattr(project, "output_dir", "."))
        backend_dir = target_dir / "backend"
        scan_target = backend_dir if backend_dir.exists() else target_dir

        audit_results = self.audit_directory(scan_target)

        # Record findings in workspace
        try:
            self.workspace.set("security_audit", audit_results)
        except Exception:
            pass

        # Record audit event in SOC2 ledger
        try:
            guardrails = get_guardrails()
            guardrails.audit_logger.record_event(
                event_type="AGENT_SECURITY_SCAN",
                action="Security Agent performed SAST code audit",
                actor_role="SYSTEM",
                resource=str(scan_target),
                status="SUCCESS" if audit_results["total_findings"] == 0 else "WARNING",
                details={
                    "files_scanned": audit_results["files_scanned"],
                    "total_findings": audit_results["total_findings"],
                },
            )
        except Exception:
            pass

        print(f"✅ Security Agent completed: {audit_results['files_scanned']} files audited, {audit_results['total_findings']} findings.")
        return audit_results