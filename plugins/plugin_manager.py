"""
Plugin Manager
"""

from analytics.generation_metrics import GenerationMetrics
from graph.change_detector import ChangeDetector
from memory.memory_manager import MemoryManager
from plugins.plugin_loader import PluginLoader


class PluginManager:

    def __init__(
        self,
        output_dir: str,
    ):

        self.output_dir = output_dir

        self.memory = MemoryManager(output_dir)

        self.detector = ChangeDetector(output_dir)

        self.metrics = GenerationMetrics()

        self.plugins = PluginLoader.load(output_dir)

    def get(
        self,
        name: str,
    ):

        return self.plugins.get(
            name.lower(),
        )

    def execute(
        self,
        plugin_name: str,
        entity_name: str,
        fields: list[str],
    ):

        plugin_name = plugin_name.lower()

        if plugin_name in self.memory.memory.completed_plugins:

            print(f"⏩ {plugin_name} already completed.")

            return

        plugin = self.get(plugin_name)

        if plugin is None:

            raise ValueError(
                f"Plugin '{plugin_name}' not found."
            )

        self.metrics.start()

        try:

            plugin.execute(

                entity_name,

                fields,

            )

            self.metrics.finish(True)

            self.memory.plugin_completed(
                plugin_name,
            )

            entity = entity_name.lower()

            file_map = {

                "model":
                f"{self.output_dir}/backend/app/models/{entity}.py",

                "schema":
                f"{self.output_dir}/backend/app/schemas/{entity}.py",

                "repository":
                f"{self.output_dir}/backend/app/repositories/{entity}_repository.py",

                "service":
                f"{self.output_dir}/backend/app/services/{entity}_service.py",

                "api":
                f"{self.output_dir}/backend/app/api/{entity}s.py",

            }

            if plugin_name in file_map:

                self.detector.register(

                    f"{entity_name}{plugin_name.title()}",

                    file_map[plugin_name],

                )

        except Exception:

            self.metrics.finish(False)

            self.memory.plugin_failed(
                plugin_name,
            )

            raise

    def report(self):

        self.metrics.report()