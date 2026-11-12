from plugins.plugin_loader import PluginLoader

plugins = PluginLoader.load(
    "outputs/Hospital_Management_System",
)

print()

print("=" * 60)

print("Loaded Plugins")

print("=" * 60)

for name in plugins:

    print(name)