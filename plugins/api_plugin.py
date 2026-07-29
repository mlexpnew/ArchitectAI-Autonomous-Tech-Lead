"""
API Plugin
"""

from pathlib import Path

from generators.ai.api_ai_generator import AIAPIGenerator

from plugins.base_plugin import BasePlugin


class APIPlugin(BasePlugin):

    def __init__(
        self,
        output_dir: str,
    ):

        super().__init__()

        self.output_dir = Path(output_dir)

        self.generator = AIAPIGenerator(
            output_dir,
        )

    @property
    def name(self):

        return "api"

    def execute(
        self,
        entity_name,
        fields,
    ):

        self.generator.generate(
            entity_name,
        )

        print("✅ API Plugin Completed")