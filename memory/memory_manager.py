"""
Memory Manager
"""

import json
from pathlib import Path

from memory.project_memory import ProjectMemory


class MemoryManager:

    def __init__(
        self,
        output_dir: str,
    ):

        self.memory_file = (
            Path(output_dir)
            / ".architect_memory.json"
        )

        self.memory = ProjectMemory()

        self.load()

    def load(self):

        if not self.memory_file.exists():
            return

        data = json.loads(
            self.memory_file.read_text(
                encoding="utf-8"
            )
        )

        self.memory.entities = data.get(
            "entities",
            {},
        )

        self.memory.generated_files = data.get(
            "generated_files",
            [],
        )

        self.memory.completed_plugins = data.get(
            "completed_plugins",
            [],
        )

        self.memory.failed_plugins = data.get(
            "failed_plugins",
            [],
        )

        self.memory.project_metadata = data.get(
            "project_metadata",
            {},
        )

    def save(self):

        self.memory_file.write_text(

            json.dumps(

                {

                    "entities": self.memory.entities,

                    "generated_files": self.memory.generated_files,

                    "completed_plugins": self.memory.completed_plugins,

                    "failed_plugins": self.memory.failed_plugins,

                    "project_metadata": self.memory.project_metadata,

                },

                indent=4,

            ),

            encoding="utf-8",

        )

    def add_entity(
        self,
        entity,
        fields,
    ):

        self.memory.entities[entity] = fields

        self.save()

    def plugin_completed(
        self,
        plugin,
    ):

        if plugin not in self.memory.completed_plugins:

            self.memory.completed_plugins.append(plugin)

            self.save()

    def plugin_failed(
        self,
        plugin,
    ):

        if plugin not in self.memory.failed_plugins:

            self.memory.failed_plugins.append(plugin)

            self.save()

    def file_generated(
        self,
        path,
    ):

        if path not in self.memory.generated_files:

            self.memory.generated_files.append(path)

            self.save()