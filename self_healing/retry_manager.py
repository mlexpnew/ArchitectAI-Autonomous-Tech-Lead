"""
Retry Manager
"""

from self_healing.healing_engine import HealingEngine


class RetryManager:

    def __init__(
        self,
        retries: int = 3,
    ):

        self.retries = retries

        self.healer = HealingEngine()

    def execute(
        self,
        code: str,
        error: str,
    ):

        current = code

        for attempt in range(
            self.retries,
        ):

            print(
                f"🔄 Retry {attempt + 1}"
            )

            valid, current, message = self.healer.heal(

                current,

                error,

            )

            if valid:

                print(
                    "✅ Recovery Successful"
                )

                return current

            error = message

        raise RuntimeError(
            "Automatic healing failed."
        )