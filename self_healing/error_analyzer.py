"""
AI Error Analyzer & Reflection Agent

Parses compiler errors, pytest failure tracebacks, and runtime exceptions
to diagnose root causes and identify the exact source file needing repair.
"""

import json
import re
from typing import Any, Dict, List, Optional
from generators.ai.code_generator import AICodeGenerator


class ErrorAnalyzer:
    """Analyzes failure contexts and returns structured reflection diagnostics."""

    def __init__(self):
        self.ai = AICodeGenerator()

    def parse_traceback_file(self, failure_context: str) -> Optional[str]:
        """
        Heuristically extracts the relative Python file path from error context.
        Matches paths like: app/api/user.py, app/models/account.py, etc.
        """
        # Look for explicit FILE: declarations first
        match = re.search(r"FILE:\s*(app/[a-zA-Z0-9_/]+\.py)", failure_context, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Look for traceback occurrences in app/
        tb_matches = re.findall(r'File\s*["\'](?:.*?/)?(app/[a-zA-Z0-9_/]+\.py)["\']', failure_context)
        if tb_matches:
            # Pick the last app/ file in the traceback stack (closest to the actual failure)
            return tb_matches[-1]

        # Look for PyCompile syntax error paths
        compile_matches = re.findall(r'(?:.*?/)?(app/[a-zA-Z0-9_/]+\.py):\s*(?:SyntaxError|IndentationError)', failure_context)
        if compile_matches:
            return compile_matches[0]

        return None

    def analyze(
        self,
        failure_context: str,
        code_context: Optional[str] = None,
        backend_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes AI reflection on the failure context and returns a structured diagnosis.
        """
        heuristic_file = self.parse_traceback_file(failure_context)

        prompt = f"""You are an autonomous Principal Tech Lead & Python/FastAPI Reflection Agent.

An automatically generated backend failed validation or tests.

Failure Context:
{failure_context}

{"Associated Code:" + chr(10) + code_context if code_context else ""}

Analyze the failure and return a structured diagnosis in EXACTLY this format:

ROOT_CAUSE:
<one or two sentences explaining the exact root cause>

FILE:
<relative path to the broken file inside app/, e.g. app/api/items.py or app/models/item.py>

ERROR_TYPE:
<SyntaxError | AssertionError | ImportError | OperationalError | LogicError>

FIX:
<precise technical instructions on how to patch the file>

CONFIDENCE:
<high | medium | low>

Rules:
- FILE must start with app/ and end with .py
- Do not wrap in markdown or backticks
- Only target files inside the app/ directory
"""

        try:
            raw_response = self.ai.generate(prompt)
        except Exception as exc:
            # Resilient fallback if AI generator is unavailable
            raw_response = f"""ROOT_CAUSE:
Encountered validation or test failure in backend code: {str(exc)}

FILE:
{heuristic_file or "app/main.py"}

ERROR_TYPE:
SyntaxError

FIX:
Clean up syntax errors, ensure valid imports, and align with FastAPI schema requirements.

CONFIDENCE:
medium
"""

        # Parse the structured response
        root_cause_m = re.search(r"ROOT_CAUSE:\s*(.+?)(?=\n[A-Z_]+:|$)", raw_response, re.DOTALL | re.IGNORECASE)
        file_m = re.search(r"FILE:\s*(app/[a-zA-Z0-9_/]+\.py)", raw_response, re.IGNORECASE)
        error_type_m = re.search(r"ERROR_TYPE:\s*(.+?)(?=\n[A-Z_]+:|$)", raw_response, re.IGNORECASE)
        fix_m = re.search(r"FIX:\s*(.+?)(?=\n[A-Z_]+:|$)", raw_response, re.DOTALL | re.IGNORECASE)

        target_file = file_m.group(1).strip() if file_m else heuristic_file
        root_cause = root_cause_m.group(1).strip() if root_cause_m else "Syntax or runtime error in generated backend."
        error_type = error_type_m.group(1).strip() if error_type_m else "RuntimeError"
        fix_suggestion = fix_m.group(1).strip() if fix_m else "Correct syntax and align type definitions."

        return {
            "root_cause": root_cause,
            "target_file": target_file,
            "error_type": error_type,
            "fix_suggestion": fix_suggestion,
            "raw_diagnosis": raw_response.strip(),
        }