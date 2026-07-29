"""
Base Plugin
"""

from abc import ABC, abstractmethod
import code

from outputs.Hospital_Management_System.backend.app.schemas import report
from self_healing.retry_manager import RetryManager
from validation.python_validator import PythonValidator
from quality.quality_gate import QualityGate


class BasePlugin(ABC):

    def __init__(self):

        self.validator = PythonValidator()

        self.retry = RetryManager()

        self.quality_gate = QualityGate()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(
        self,
        entity_name: str,
        fields: list[str],
    ):
        pass

    def validate_and_fix(
        self,
        code: str,
    ):

        valid, error = self.validator.validate(
            code,
        )

        if valid:

            report = self.quality.check(code)

            if report.passed:

                return code

            print()

            print("Quality Score:", report.score)

            for issue in report.issues:

                print("-", issue)

            return self.retry.execute(
    code,
    "\n".join(report.issues),
)

        print("⚠️ Invalid code detected.")

        return self.retry.execute(
            code,
            error,
        )