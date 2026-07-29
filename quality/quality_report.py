from dataclasses import dataclass


@dataclass
class QualityReport:

    passed: bool

    score: int

    issues: list[str]