"""
Plugin Loader

Automatically discovers ArchitectAI plugins.
"""

import importlib
import inspect
import pkgutil

import plugins as plugins_package

from plugins.base_plugin import BasePlugin


class PluginLoader:

    @staticmethod
    def load(output_dir: str):

        loaded_plugins = {}

        for _, module_name, _ in pkgutil.iter_modules(
            plugins_package.__path__
        ):

            if module_name in {
                "__init__",
                "base_plugin",
                "plugin_loader",
                "plugin_manager",
            }:
                continue

            module = importlib.import_module(
                f"plugins.{module_name}"
            )

            for _, cls in inspect.getmembers(
                module,
                inspect.isclass,
            ):

                if (
                    issubclass(cls, BasePlugin)
                    and cls is not BasePlugin
                ):

                    instance = cls(output_dir)

                    loaded_plugins[
                        instance.name.lower()
                    ] = instance

        return loaded_plugins