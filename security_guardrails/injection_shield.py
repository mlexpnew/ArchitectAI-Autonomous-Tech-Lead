"""
Enterprise Security Guardrails: Adversarial Prompt Injection & Jailbreak Shield

Detects and neutralizes prompt injections, system prompt exfiltration attempts,
DAN jailbreak patterns, and role-override exploits before they reach LLM reasoning engines.
"""

import re
from typing import Dict, List, Tuple


class PromptInjectionBlockedException(Exception):
    """Raised when an adversarial prompt injection attempt is detected and blocked."""
    def __init__(self, message: str, threat_type: str, score: float):
        super().__init__(message)
        self.threat_type = threat_type
        self.score = score


class PromptInjectionShield:
    """
    Multi-layered heuristics and pattern matching engine for detecting
    adversarial prompt injection attacks and system instruction overrides.
    """

    # High-confidence attack signatures
    ATTACK_PATTERNS = [
        # Instruction overrides
        (r"(?i)\bignore\s+(all\s+)?(previous|prior|above)\s+(instructions|directives|prompts|rules)\b", "INSTRUCTION_OVERRIDE", 0.95),
        (r"(?i)\bdisregard\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules|commands)\b", "INSTRUCTION_OVERRIDE", 0.95),
        (r"(?i)\bforget\s+(all\s+)?(previous|prior|above)\s+(instructions|guidelines|rules)\b", "INSTRUCTION_OVERRIDE", 0.95),
        (r"(?i)\bdo\s+not\s+follow\s+(the\s+)?(above|previous|initial)\s+instructions\b", "INSTRUCTION_OVERRIDE", 0.90),
        
        # Jailbreak personas
        (r"(?i)\byou\s+are\s+now\s+(in\s+)?(DAN|developer|unfiltered|jailbroken|god)\s+mode\b", "JAILBREAK_PERSONA", 0.98),
        (r"(?i)\bact\s+as\s+an?\s+unfiltered|uncensored|unrestricted\s+(ai|model|assistant)\b", "JAILBREAK_PERSONA", 0.95),
        (r"(?i)\bpretend\s+you\s+have\s+no\s+(rules|limits|safety|filters|constraints)\b", "JAILBREAK_PERSONA", 0.95),
        (r"(?i)\balways\s+say\s+yes\s+to\s+everything\b", "JAILBREAK_PERSONA", 0.85),
        
        # System prompt exfiltration
        (r"(?i)\b(reveal|print|repeat|show|output|leak)\s+(your\s+)?(system\s+prompt|initial\s+instructions|system\s+instructions)\b", "PROMPT_EXFILTRATION", 0.92),
        (r"(?i)\bwhat\s+(are|were)\s+your\s+(original|system|initial)\s+(instructions|prompts|rules)\b", "PROMPT_EXFILTRATION", 0.90),
        
        # Delimiter manipulation & simulated system tokens
        (r"(?i)<\s*system\s*>|<\s*/\s*system\s*>", "SIMULATED_SYSTEM_TOKEN", 0.90),
        (r"(?i)\[\s*system\s*\]|\[\s*/\s*system\s*\]", "SIMULATED_SYSTEM_TOKEN", 0.88),
        (r"(?i)```\s*system\b", "SIMULATED_SYSTEM_TOKEN", 0.85),
        (r"(?i)\bhuman:\s*.*\bai:\s*", "CONVERSATION_SPOOFING", 0.85),
    ]

    # Suspicious keywords that elevate risk score when combined
    SUSPICIOUS_KEYWORDS = [
        "bypass", "override", "root access", "sudo", "jailbreak",
        "uncensored", "backdoor", "exploit", "disable security", "unrestricted"
    ]

    def __init__(self, strict_mode: bool = False, threshold: float = 0.80):
        self.strict_mode = strict_mode
        self.threshold = threshold

    def scan(self, text: str) -> Dict[str, any]:
        """
        Scans input text for adversarial prompt injection patterns.
        
        Returns:
            dict containing:
                - is_safe (bool)
                - threat_score (float 0.0 - 1.0)
                - threat_type (str or None)
                - matched_patterns (list of str)
                - action_taken (str: 'ALLOWED' | 'FLAGGED' | 'BLOCKED')
        """
        if not text or not isinstance(text, str):
            return {
                "is_safe": True,
                "threat_score": 0.0,
                "threat_type": None,
                "matched_patterns": [],
                "action_taken": "ALLOWED",
            }

        max_score = 0.0
        primary_threat = None
        matched_patterns = []

        # Check explicit attack patterns
        for pattern, threat_type, score in self.ATTACK_PATTERNS:
            match = re.search(pattern, text)
            if match:
                matched_patterns.append(match.group(0))
                if score > max_score:
                    max_score = score
                    primary_threat = threat_type

        # Check cumulative suspicious keywords if no high-severity match
        if max_score < self.threshold:
            keyword_hits = [kw for kw in self.SUSPICIOUS_KEYWORDS if kw in text.lower()]
            if len(keyword_hits) >= 2:
                max_score = min(0.75 + (len(keyword_hits) * 0.05), 0.90)
                primary_threat = "SUSPICIOUS_KEYWORDS_ACCUMULATION"
                matched_patterns.extend(keyword_hits)

        is_safe = max_score < self.threshold
        action = "ALLOWED" if is_safe else ("BLOCKED" if self.strict_mode or max_score >= 0.90 else "FLAGGED")

        return {
            "is_safe": is_safe,
            "threat_score": round(max_score, 3),
            "threat_type": primary_threat,
            "matched_patterns": matched_patterns,
            "action_taken": action,
        }

    def sanitize_or_raise(self, text: str) -> str:
        """
        Validates text and raises PromptInjectionBlockedException if an attack is detected.
        Otherwise returns clean text.
        """
        scan_result = self.scan(text)
        if not scan_result["is_safe"]:
            raise PromptInjectionBlockedException(
                f"Adversarial prompt injection detected: {scan_result['threat_type']} (score: {scan_result['threat_score']})",
                threat_type=scan_result["threat_type"],
                score=scan_result["threat_score"],
            )
        return text
