"""
Service Plugin
"""

from pathlib import Path

from generators.ai.service_ai_generator import AIServiceGenerator

from plugins.base_plugin import BasePlugin


class ServicePlugin(BasePlugin):

    def __init__(
        self,
        output_dir: str,
    ):

        super().__init__()

        self.output_dir = Path(output_dir)

        self.generator = AIServiceGenerator(
            output_dir,
        )

    @property
    def name(self):

        return "service"

    def execute(
        self,
        entity_name,
        fields,
    ):

        self.generator.generate(
            entity_name,
        )

        print("✅ Service Plugin Completed")