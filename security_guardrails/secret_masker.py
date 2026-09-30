"""
Enterprise Security Guardrails: PII, Secrets & High-Entropy Credential Masker

Redacts credentials, private keys, database connection secrets, and PII from prompts,
LLM outputs, and persisted logs to maintain zero-data-leakage compliance (SOC2 / HIPAA).
"""

import re
from typing import Dict, List, Tuple


class SecretMasker:
    """
    Scans text for sensitive corporate secrets, cloud credentials, tokens, and PII,
    replacing them with standardized redaction tokens (e.g., [REDACTED_AWS_KEY]).
    """

    SECRET_PATTERNS = [
        # Cloud & Provider Credentials
        ("AWS_ACCESS_KEY", r"\b(AKIA[0-9A-Z]{16})\b", "[REDACTED_AWS_KEY]"),
        ("AWS_SECRET_KEY", r"(?i)aws_secret_access_key\s*[:=]\s*([a-zA-Z0-9/+=]{40})", "aws_secret_access_key=[REDACTED_AWS_SECRET]"),
        ("GITHUB_PAT", r"\b(ghp_[a-zA-Z0-9]{36}|gho_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82})\b", "[REDACTED_GITHUB_TOKEN]"),
        ("OPENAI_KEY", r"\b(sk-proj-[a-zA-Z0-9_\-]{40,}|sk-[a-zA-Z0-9]{32,48})\b", "[REDACTED_OPENAI_KEY]"),
        ("ANTHROPIC_KEY", r"\b(sk-ant-[a-zA-Z0-9_\-]{40,})\b", "[REDACTED_ANTHROPIC_KEY]"),
        ("GROQ_KEY", r"\b(gsk_[a-zA-Z0-9]{48,64})\b", "[REDACTED_GROQ_KEY]"),
        
        # Cryptographic Private Keys
        ("PRIVATE_KEY", r"-----BEGIN (?:RSA|EC|DSA|OPENSSH) PRIVATE KEY-----[\s\S]*?-----END (?:RSA|EC|DSA|OPENSSH) PRIVATE KEY-----", "[REDACTED_PRIVATE_KEY]"),
        
        # Database URIs with Passwords
        ("DATABASE_URI_PASSWORD", r"(?i)(postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://([^:\s]+):([^@\s]+)@([^\s/]+)", r"\1://\2:[REDACTED_DB_PWD]@\4"),
        
        # Bearer / JWT Tokens
        ("JWT_TOKEN", r"\b(eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b", "[REDACTED_JWT_TOKEN]"),
        
        # PII: US Social Security Number (SSN)
        ("PII_SSN", r"\b(\d{3}-\d{2}-\d{4})\b", "[REDACTED_SSN]"),
        
        # PII: Standard Credit Card Formats (13-16 digits with dashes or spaces)
        ("PII_CREDIT_CARD", r"\b(?:\d{4}[-\s]?){3}\d{4}\b", "[REDACTED_CREDIT_CARD]"),
        
        # Generic Secret Key Assignments in code/config
        ("GENERIC_SECRET_ASSIGN", r"(?i)(password|secret|api_key|token|auth_token)\s*[:=]\s*['\"]([a-zA-Z0-9_\-!@#$%^&*()]{8,})['\"]", r'\1="[REDACTED_SECRET]"'),
    ]

    def __init__(self, mask_pii: bool = True):
        self.mask_pii = mask_pii

    def mask(self, text: str) -> Tuple[str, int, List[str]]:
        """
        Scans and redacts all secrets and PII from the text.
        
        Returns:
            Tuple of:
                - masked_text (str)
                - total_redactions_count (int)
                - detected_types (list of str)
        """
        if not text or not isinstance(text, str):
            return text, 0, []

        redacted_text = text
        detected_types = []
        total_count = 0

        for secret_name, pattern, replacement in self.SECRET_PATTERNS:
            if not self.mask_pii and secret_name.startswith("PII_"):
                continue

            matches = list(re.finditer(pattern, redacted_text))
            if matches:
                total_count += len(matches)
                if secret_name not in detected_types:
                    detected_types.append(secret_name)
                
                # Apply substitution
                redacted_text = re.sub(pattern, replacement, redacted_text)

        return redacted_text, total_count, detected_types

    def contains_secrets(self, text: str) -> bool:
        """Quick boolean probe to check if text contains unmasked sensitive credentials."""
        _, count, _ = self.mask(text)
        return count > 0
