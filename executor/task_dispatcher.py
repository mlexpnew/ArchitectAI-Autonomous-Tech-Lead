"""
Task Dispatcher

Dispatches execution to ArchitectAI plugins.
"""

from plugins.plugin_manager import PluginManager


class TaskDispatcher:

    def __init__(
        self,
        output_dir: str,
    ):

        self.plugin_manager = PluginManager(
            output_dir,
        )

    def dispatch(
        self,
        task,
        entity_name: str,
        fields: list[str],
    ):

        print(f"\n🚀 Step {task.step}")

        print(f"Task: {task.title}")

        title = task.title.lower()

        mapping = {

            "generate models": "model",

            "generate model": "model",

            "generate schemas": "schema",

            "generate schema": "schema",

            "generate repository": "repository",

            "generate repositories": "repository",

            "generate service": "service",

            "generate services": "service",

            "generate api": "api",

            "generate apis": "api",

        }

        plugin_name = mapping.get(title)

        if plugin_name is None:

            print(f"⚠️ No plugin mapped for '{task.title}'")

            return

        self.plugin_manager.execute(

            plugin_name,

            entity_name,

            fields,

        )