"""
Repository Plugin
"""

from pathlib import Path

from generators.ai.repository_ai_generator import AIRepositoryGenerator

from plugins.base_plugin import BasePlugin


class RepositoryPlugin(BasePlugin):

    def __init__(
        self,
        output_dir: str,
    ):

        super().__init__()

        self.output_dir = Path(output_dir)

        self.generator = AIRepositoryGenerator(
            output_dir,
        )

    @property
    def name(self):

        return "repository"

    def execute(
        self,
        entity_name,
        fields,
    ):

        self.generator.generate(
            entity_name,
        )

        print("✅ Repository Plugin Completed")