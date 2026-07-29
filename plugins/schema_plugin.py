"""
Schema Plugin
"""

from pathlib import Path

from generators.ai.schema_ai_generator import AISchemaGenerator

from plugins.base_plugin import BasePlugin


class SchemaPlugin(BasePlugin):

    def __init__(
        self,
        output_dir: str,
    ):

        super().__init__()

        self.output_dir = Path(output_dir)

        self.generator = AISchemaGenerator(
            output_dir,
        )

    @property
    def name(self):

        return "schema"

    def execute(
        self,
        entity_name,
        fields,
    ):

        self.generator.generate(

            entity_name,

            fields,

        )

        print("✅ Schema Plugin Completed")