"""
Quality Gate
"""

import ast

from quality.quality_report import QualityReport


class QualityGate:

    def check(
        self,
        code: str,
    ) -> QualityReport:

        issues = []

        try:
            ast.parse(code)
        except Exception as e:
            issues.append(str(e))

        forbidden = [

            "```",

            "However",

            "Explanation",

            "Here is",

            "Hope this helps",

            "Note:",

        ]

        for item in forbidden:

            if item in code:
                issues.append(
                    f"Forbidden text: {item}"
                )

        if len(code.splitlines()) < 5:

            issues.append(
                "Generated file is too small."
            )

        score = max(
            0,
            100 - len(issues) * 20,
        )

        return QualityReport(

            passed=len(issues) == 0,

            score=score,

            issues=issues,

        )