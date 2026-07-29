"""
Healing Engine
"""

from review.code_fixer import CodeFixer
from validation.python_validator import PythonValidator


class HealingEngine:

    def __init__(self):

        self.fixer = CodeFixer()

    def heal(
        self,
        code: str,
        error: str,
    ):

        fixed = self.fixer.fix(
            code,
            error,
        )

        valid, message = PythonValidator.validate(
            fixed,
        )

        return valid, fixed, message