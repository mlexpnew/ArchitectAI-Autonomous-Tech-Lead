"""
Model Plugin
"""

from pathlib import Path

from generators.ai.model_ai_generator import AIModelGenerator

from plugins.base_plugin import BasePlugin


class ModelPlugin(BasePlugin):

    def __init__(
        self,
        output_dir: str,
    ):

        super().__init__()

        self.output_dir = Path(output_dir)

        self.generator = AIModelGenerator(
            output_dir,
        )

    @property
    def name(self):

        return "model"

    def execute(
        self,
        entity_name,
        fields,
    ):

        self.generator.generate(

            entity_name,

            fields,

        )

        print("✅ Model Plugin Completed")