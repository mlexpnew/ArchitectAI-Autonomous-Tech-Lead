"""
Quality Controller
"""

from quality.critic_agent import CriticAgent
from review.code_fixer import CodeFixer


class QualityController:

    def __init__(self):

        self.critic = CriticAgent()

        self.fixer = CodeFixer()

    def improve(
        self,
        code: str,
    ):

        attempts = 3

        for _ in range(attempts):

            report = self.critic.review(code)

            print(
                f"⭐ Score: {report['score']}"
            )

            if report["approved"]:

                return code

            issues = "\n".join(
                report["issues"]
            )

            code = self.fixer.fix(
                code,
                issues,
            )

        return code