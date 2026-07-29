"""
Robust JSON Parser
"""

import json


class JSONParser:

    @staticmethod
    def parse(text: str):

        text = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        start = text.find("[")

        if start == -1:
            start = text.find("{")

        if start == -1:
            raise ValueError("No JSON found.")

        depth = 0

        end = start

        for i in range(start, len(text)):

            if text[i] in "[{":
                depth += 1

            elif text[i] in "]}":
                depth -= 1

                if depth == 0:
                    end = i + 1
                    break

        return json.loads(text[start:end])